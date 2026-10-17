import os
from datetime import datetime

import pika


QUEUE_NAME = "iot_lab_queue"


def connect_to_broker():
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "guest"),
        os.getenv("RABBITMQ_PASSWORD", "guest"),
    )
    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        virtual_host=os.getenv("RABBITMQ_VHOST", "/"),
        credentials=credentials,
    )
    return pika.BlockingConnection(parameters)


def on_message(channel, method, properties, body):
    message = body.decode("utf-8")
    received_at = datetime.now().strftime("%H:%M:%S")
    print(f"Da nhan message: {message}")
    print(f"Thoi gian nhan: {received_at}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = connect_to_broker()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    print(f"Dang lang nghe queue {QUEUE_NAME}. Nhan Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Da dung consumer.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()