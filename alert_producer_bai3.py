import os

import pika


EXCHANGE_NAME = "iot_alert_exchange"
ALERTS = [
    ("info", "He thong IoT hoat dong binh thuong"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]


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
        channel.exchange_declare(
            exchange=EXCHANGE_NAME,
            exchange_type="direct",
        )
        for routing_key, message in ALERTS:
            channel.basic_publish(
                exchange=EXCHANGE_NAME,
                routing_key=routing_key,
                body=message.encode("utf-8"),
                properties=pika.BasicProperties(content_type="text/plain"),
            )
            print(f"Da gui [{routing_key}]: {message}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()