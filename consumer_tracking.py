from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'tracking-service',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['driver-location'])

print("Tracking service running...")

while True:
    msg = consumer.poll(1.0)

    if msg and not msg.error():
        data = json.loads(msg.value().decode('utf-8'))
        print("Driver Location:", data)