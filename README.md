# IoT Buoi 2 - Python voi AMQP

## Yeu cau

- Python 3
- RabbitMQ dang chay tren may local hoac broker do lop cung cap
- Thu vien Python `pika`

Cai thu vien:

```cmd
py -m pip install pika
```

Mac dinh cac chuong trinh ket noi den `localhost:5672`, virtual host `/`, tai khoan `guest` va mat khau `guest`. Neu dung broker khac, dat cac bien moi truong nay trong moi cua so terminal truoc khi chay chuong trinh:

```cmd
set RABBITMQ_HOST=localhost
set RABBITMQ_PORT=5672
set RABBITMQ_USER=guest
set RABBITMQ_PASSWORD=guest
set RABBITMQ_VHOST=/
```

RabbitMQ mac dinh han che tai khoan `guest` ket noi tu may khac. Neu broker nam tren may chu/lop, hay dung tai khoan va thong tin ket noi duoc cap.

## Bai 1 - Queue co ban

Mo mot terminal va chay consumer truoc:

```cmd
py consumer_bai1.py
```

Mo terminal khac, thay ho ten va ma sinh vien trong `producer_bai1.py`, sau do chay:

```cmd
py producer_bai1.py
```

Consumer se in noi dung message va thoi diem nhan tu queue `iot_lab_queue`.

## Bai 2 - Du lieu cam bien

Chay monitoring consumer:

```cmd
py monitor_consumer_bai2.py
```

Mo terminal khac va chay sensor producer:

```cmd
py sensor_producer_bai2.py
```

Producer gui JSON vao `sensor_data_queue` moi 3 giay. Consumer hien thi nhiet do, do am va canh bao khi nhiet do lon hon 35 hoac do am nho hon 40. Du lieu duoc sinh ngau nhien nen khong nhat thiet co canh bao ngay lap tuc.

## Bai 3 - Dinh tuyen canh bao

Mo ba terminal va chay hai consumer truoc:

```cmd
py warning_consumer_bai3.py
```

```cmd
py critical_consumer_bai3.py
```

Sau do chay producer trong terminal thu ba:

```cmd
py alert_producer_bai3.py
```

Exchange `iot_alert_exchange` la direct exchange. `warning` chi duoc bind den `warning_queue`; `critical` chi duoc bind den `critical_queue`. Message `info` khong duoc hai queue nay nhan.

Nhan `Ctrl+C` de dung cac consumer va sensor producer.

## Danh sach chuong trinh

- `producer_bai1.py`, `consumer_bai1.py`
- `sensor_producer_bai2.py`, `monitor_consumer_bai2.py`
- `alert_producer_bai3.py`, `warning_consumer_bai3.py`, `critical_consumer_bai3.py`

## Ket qua kiem tra

Khi chay, xac nhan Bai 1 nhan du payload va in thoi gian; Bai 2 nhan duoc JSON va canh bao dung nguong; Bai 3 chi chuyen warning/critical den consumer tuong ung. Broker phai duoc bat truoc khi chay cac chuong trinh.
