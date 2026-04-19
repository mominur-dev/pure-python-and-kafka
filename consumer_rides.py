from confluent_kafka import Consumer
import json

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ride-service',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['ride-request'])

print("Ride matching service running...")

while True:
    msg = consumer.poll(1.0)

    if msg and not msg.error():
        data = json.loads(msg.value().decode('utf-8'))
        print("New Ride Request:", data)