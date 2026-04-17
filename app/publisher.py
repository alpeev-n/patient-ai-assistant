import json
import os
import pika


def publish_ml_task(message: dict) -> None:
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=os.getenv("RABBITMQ_PORT"),
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_DEFAULT_USER"), os.getenv("RABBITMQ_DEFAULT_PASS")
            ),
        )
    ) as connection:
        channel = connection.channel()

        channel.queue_declare(queue="ml_tasks", durable=True)

        channel.basic_publish(
            exchange="",
            routing_key="ml_tasks",
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2),
        )
