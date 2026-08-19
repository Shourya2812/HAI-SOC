import json

from bson import ObjectId
from kafka import KafkaProducer

from backend.app.database.collections import logs_collection


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "healthcare-security-logs"


def json_serializer(data):
    return json.dumps(data, default=str).encode("utf-8")


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=json_serializer,
    )


def publish_logs():

    producer = create_producer()

    logs = logs_collection.find()

    count = 0

    for log in logs:

        log["id"] = str(log.pop("_id"))

        future = producer.send(
            KAFKA_TOPIC,
            value=log,
        )

        metadata = future.get(timeout=10)

        print(
            f"Published log {log['id']} "
            f"-> partition={metadata.partition}, "
            f"offset={metadata.offset}"
        )

        count += 1

    producer.flush()

    producer.close()

    print(
        f"\nPublished {count} logs to "
        f"'{KAFKA_TOPIC}'"
    )


if __name__ == "__main__":
    publish_logs()