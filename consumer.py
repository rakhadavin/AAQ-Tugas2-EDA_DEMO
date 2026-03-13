import pika
import json
import os
import time
def callback(ch, method, properties, body):
    job = json.loads(body)
    print(f" [v] Received job ID {job['job_id']}: Processing {job['job']}...")
    # Simulate processing logic
    print(f" [!] job {job['job_id']} Processed Successfully.")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_distribution')
channel.basic_consume(queue='task_distribution', on_message_callback=callback, auto_ack=True)
def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f" [v] Consumer {os.getpid()} started: {data['job']}")
    
    # Simulate work
    time.sleep(data['sleep'])
    
    print(f" [!] Consumer {os.getpid()} finished: {data['job']}")
    # Manual acknowledgment: tells RabbitMQ the job is done
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_distribution', on_message_callback=callback)
print(' [*] Waiting for events. To exit press CTRL+C')
channel.start_consuming()