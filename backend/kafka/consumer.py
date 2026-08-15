import json

from kafka import KafkaConsumer
from pymongo.errors import DuplicateKeyError

from ml.models.predict import Predictor
from backend.app.services.anomaly_service import AnomalyService
from backend.app.services.incident_service import IncidentService


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "healthcare-security-logs"
KAFKA_GROUP_ID = "hai-soc-ml-consumer"


def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
    )


def consume_logs():

    consumer = create_consumer()

    print(f"Listening to topic: {KAFKA_TOPIC}")
    print(f"Consumer group: {KAFKA_GROUP_ID}")
    print("Waiting for messages...\n")

    try:

        for message in consumer:

            log = message.value

            print(
                f"Received log | "
                f"partition={message.partition} | "
                f"offset={message.offset}"
            )

            print(
                f"  id={log.get('id')} | "
                f"source={log.get('source')} | "
                f"action={log.get('action')} | "
                f"severity={log.get('severity')}"
            )

            # -----------------------------------------
            # K5.2 — ML INFERENCE
            # -----------------------------------------

            prediction = Predictor.predict(log)

            print(
                f"  ML model={prediction['model']} | "
                f"prediction={prediction['prediction']} | "
                f"anomaly={prediction['is_anomaly']} | "
                f"score={prediction['score']:.4f}"
            )

            # -----------------------------------------
            # K5.7 — APPLICATION-LEVEL IDEMPOTENCY
            # -----------------------------------------

            try:

                anomaly_record = AnomalyService.save_prediction(
                    log_id=log["id"],
                    detector=prediction["model"],
                    prediction=prediction["prediction"],
                    anomaly_score=prediction["score"],
                )

                if prediction["is_anomaly"]:
                    incident = IncidentService.create_from_prediction(
                        log_id=log["id"],
                        detector=prediction["model"],
                        anomaly_score=prediction["score"],
                        title=f"Security Anomaly: {log.get('action', 'Event')}",
                        description=(
                            f"Anomalous activity detected in "
                            f"{log.get('source', 'Unknown')} "
                            f"by {prediction['model']}."
                        ),
                    )

                    print(
                        f"  🚨 Incident created | "
                        f"id={incident.id} | "
                        f"risk={incident.risk_level}"
                    )

                consumer.commit()

                print(
                    f"  Anomaly record saved & committed | "
                    f"id={anomaly_record.id} | "
                    f"log_id={anomaly_record.log_id}"
                )

            except DuplicateKeyError:

                consumer.commit()

                print(
                    f"  [INFO] Event log_id={log.get('id')} "
                    f"(detector={prediction['model']}) already processed. "
                    f"Offset committed."
                )

            print()

    except KeyboardInterrupt:
        print("\nConsumer stopped.")

    finally:
        consumer.close()


if __name__ == "__main__":
    consume_logs()