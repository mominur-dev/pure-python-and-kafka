from confluent_kafka import Producer
import json
import time

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def send(topic, data):
    producer.produce(topic, json.dumps(data).encode('utf-8'))
    producer.poll(0)

# Simulated system loop
while True:
    
    # Driver location
    send("driver-location", {
        "driver_id": 101,
        "lat": 23.81,
        "lng": 90.41
    })

    # Ride request
    send("ride-request", {
        "user_id": 55,
        "pickup": "Mohakhali",
        "drop": "Gulshan 1"
    })

    # Payment event
    send("payments", {
        "ride_id": 999,
        "amount": 150
    })

    print("Events sent")
    time.sleep(3)