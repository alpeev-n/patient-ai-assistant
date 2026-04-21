from dotenv import load_dotenv

load_dotenv()
import json
import os
import pika

from app.database import SessionLocal
from app.db.models.ml_task import MLTask
from app.models.enums import TaskStatus
from app.models.ml_model import PatientAssistantModel

ml_model = PatientAssistantModel(
    id="patient_assistant_v1",
    name="Patient Assistant",
    description="Zero-shot triage model",
    cost_per_prediction=0.01,
)


def process_message(ch, method, properties, body):
    db = SessionLocal()

    try:
        message = json.loads(body)
        task_id = message.get("task_id")
        input_data = message.get("features", {})

        task = db.query(MLTask).filter(MLTask.id == task_id).first()

        if task:
            result = ml_model.predict(input_data)

            task.status = TaskStatus.DONE
            task.result = result

            db.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Task {task_id} processed successfully", flush=True)
        else:
            print(f"Task {task_id} not found in DB")

    except Exception as e:
        import traceback

        print(f"Error processing task: {e}", flush=True)
        print(traceback.format_exc(), flush=True)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    finally:
        db.close()


def start_worker():
    print("[*] Waiting for messages...", flush=True)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv("RABBITMQ_HOST"),
            port=int(os.getenv("RABBITMQ_PORT", 5672)),
            credentials=pika.PlainCredentials(
                os.getenv("RABBITMQ_DEFAULT_USER", "guest"),
                os.getenv("RABBITMQ_DEFAULT_PASS", "guest"),
            ),
        )
    )

    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    queue_name = "ml_tasks"
    channel.queue_declare(queue=queue_name, durable=True)

    print(f"[*] Waiting for messages in {queue_name}. To exit press CTRL+C")

    channel.basic_consume(queue=queue_name, on_message_callback=process_message)
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
