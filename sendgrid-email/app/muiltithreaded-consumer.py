import pika
import threading
import json
from config import rabbitmq_config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template
import smtplib
from tenacity import retry, stop_after_attempt, wait_fixed

class Consumer:
    def __init__(self, queue_name, num_threads):
        self.queue_name = queue_name
        self.num_threads = num_threads
        self.connection_params = pika.ConnectionParameters(host="localhost")

    def on_message(self, channel, method, properties, body):
        print(f"Thread: {threading.current_thread().name}, Received: {body}")
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self):
        connection = pika.BlockingConnection(self.connection_params)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message)

        print(f"Thread: {threading.current_thread().name} - Waiting for messages")
        channel.start_consuming()

    def start(self):
        for i in range(self.num_threads):
            thread_name = f"Consumer-{i+1}"
            thread = threading.Thread(target=self.consume, name=thread_name)
            thread.start()

if __name__ == "__main__":
    queue_name = "test_queue"
    num_threads = 4

    consumer = Consumer(queue_name, num_threads)
    consumer.start()