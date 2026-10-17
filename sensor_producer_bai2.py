import json
import os
import random
import time

import pika


QUEUE_NAME = "sensor_data_queue"
DEVICE_ID = "sensor01"


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
        print(f"Dang gui du lieu den {QUEUE_NAME} moi 3 giay. Nhan Ctrl+C de dung.")
        while True:
            reading = {
                "device_id": DEVICE_ID,
                "temperature": round(random.uniform(20.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
            }
            body = json.dumps(reading).encode("utf-8")
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE_NAME,
                body=body,
                properties=pika.BasicProperties(content_type="application/json"),
            )
            print(f"Da gui: {body.decode('utf-8')}")
            time.sleep(3)
    except KeyboardInterrupt:
        print("Da dung sensor producer.")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()