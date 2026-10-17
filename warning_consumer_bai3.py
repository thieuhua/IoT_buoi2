import os

import pika


EXCHANGE_NAME = "iot_alert_exchange"
QUEUE_NAME = "warning_queue"
ROUTING_KEY = "warning"


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
    print(f"[{QUEUE_NAME}] Da nhan: {body.decode('utf-8')}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = connect_to_broker()
    try:
        channel = connection.channel()
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type="direct",
        )
        channel.queue_declare(queue=QUEUE_NAME)
        channel.queue_bind(
            exchange=EXCHANGE_NAME,
            queue=QUEUE_NAME,
            routing_key=ROUTING_KEY,
        )
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
        print(f"Dang lang nghe {QUEUE_NAME} ({ROUTING_KEY}). Nhan Ctrl+C de dung.")
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Da dung warning consumer.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()