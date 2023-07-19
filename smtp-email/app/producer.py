import pika
import json
from config import rabbitmq_config
import logging

logging.basicConfig(level=logging.INFO)

def publish_task(subject, to_email, template, context):
    logging.info(f"Publishing task: {subject} {to_email} {template} {context}")
    task = {
        'subject': subject,
        'to_email': to_email,
        'template': template,
        'context': context
    }

    logging.info(f"Connecting to RabbitMQ server {rabbitmq_config['host']}:{rabbitmq_config['port']}")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_config['host'],
            port=rabbitmq_config['port'],
            credentials=pika.PlainCredentials(
                rabbitmq_config['username'],
                rabbitmq_config['password']
            )
        )
    )



    channel = connection.channel()
    channel.queue_declare(  queue=rabbitmq_config['queue'],
                            durable=True,
                            arguments={
                                'x-dead-letter-exchange': rabbitmq_config['dead_letter_exchange'],
                                'x-dead-letter-routing-key': rabbitmq_config['dead_letter_routing_key']
                            }
    )
    logging.info(f"Connected to RabbitMQ server {rabbitmq_config['host']}:{rabbitmq_config['port']}")
    logging.info(f"Publishing task: {task}")
    logging.info(f"Publishing to exchange {rabbitmq_config['exchange']} with routing key {rabbitmq_config['routing_key']}")
    channel.basic_publish(
        exchange=rabbitmq_config['exchange'],
        routing_key=rabbitmq_config['routing_key'],
        body=json.dumps(task),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make message persistent
        )
    )

    connection.close()
