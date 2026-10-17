import os

import pika


QUEUE_NAME = "iot_lab_queue"
MESSAGE = "Xin chao tu ung dung Python AMQP - B21xxxx - Nguyen Van A"


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


def main():
    connection = connect_to_broker()
    try:
        channel = connection.channel()
        channel.queue_declare(queue=QUEUE_NAME)
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=MESSAGE.encode("utf-8"),
        )
        print(f"Da gui message: {MESSAGE}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()