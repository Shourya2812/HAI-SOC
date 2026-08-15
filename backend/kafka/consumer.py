import json

from kafka import KafkaConsumer


KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "healthcare-security-logs"
KAFKA_GROUP_ID = "hai-soc-consumer"


def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
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
                f"  source={log.get('source')} | "
                f"action={log.get('action')} | "
                f"severity={log.get('severity')} | "
                f"outcome={log.get('outcome')}"
            )

            print()

    except KeyboardInterrupt:
        print("\nConsumer stopped.")

    finally:
        consumer.close()


if __name__ == "__main__":
    consume_logs()