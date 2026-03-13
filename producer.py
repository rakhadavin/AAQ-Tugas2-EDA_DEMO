import pika
import json
import time

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Create a queue
channel.queue_declare(queue='task_distribution')

tasks = [
    {"job_id": 1, "job": "Send Welcome Email", "sleep": 1},
    {"job_id": 2, "job": "Process Profile Image", "sleep": 5},
    {"job_id": 3, "job": "Generate Monthly Report", "sleep": 3},
    {"job_id": 4, "job": "Sync Data to Cloud", "sleep": 2},
]

for task in tasks:
    message = json.dumps(task)
    channel.basic_publish(
        exchange='',
        routing_key='task_distribution',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print(f" [PRODUCER] Dispatched: {task['job']} (ID: {task['job_id']})")
    time.sleep(0.5)

connection.close()