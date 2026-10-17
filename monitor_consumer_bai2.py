import json
import os

import pika


QUEUE_NAME = "sensor_data_queue"


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
    try:
        reading = json.loads(body.decode("utf-8"))
        device_id = reading["device_id"]
        temperature = float(reading["temperature"])
        humidity = float(reading["humidity"])

        print(f"Device: {device_id}")
        print(f"Temperature: {temperature:.1f}")
        print(f"Humidity: {humidity:.1f}")
        if temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity < 40:
            print("CANH BAO: Do am thap")
        print()
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Du lieu cam bien khong hop le: {error}")
    finally:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = connect_to_broker()
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
    print(f"Dang lang nghe queue {QUEUE_NAME}. Nhan Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Da dung monitoring consumer.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()