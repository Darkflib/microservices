import pika
import json
from config import rabbitmq_config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
import os
import dotenv
import sendgrid
from sendgrid.helpers.mail import *

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

dotenv.load_dotenv()

FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_NAME = os.environ.get('FROM_NAME')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')


@retry(stop=stop_after_attempt(3), wait=wait_fixed(60))
def send_email_with_retry(subject, to_email, template, context):

    logging.info(f"Sending email to {to_email} with subject {subject}")

    from_email = FROM_EMAIL

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with app.app_context():
        html_content = render_template(template, **context)

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
    data = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email
                    }
                ],
                "subject": subject
            }
        ],
        "from": {
            "email": from_email,
            "name": FROM_NAME
        },
        "content": [
            {
                "type": "text/html",
                "value": html_content
            }
        ]
    }
    response = sg.client.mail.send.post(request_body=data)
    logging.info(f"Email sent to {to_email} with subject {subject} with status code {response.status_code}")
    logging.debug(f"Email sent to {to_email} with subject {subject} with response body {response.body}")
    logging.debug(f"Email sent to {to_email} with subject {subject} with response headers {response.headers}")
    


def send_email(subject, to_email, template, context):
    try:
        send_email_with_retry(subject, to_email, template, context)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def on_message(channel, method, properties, body):
    task = json.loads(body)
    success = send_email(task['subject'], task['to_email'], task['template'], task['context'])
    if success:
        channel.basic_ack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

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

# Declare dead-letter exchange and queue
channel.exchange_declare(exchange=rabbitmq_config['dead_letter_exchange'], exchange_type='direct')
channel.queue_declare(queue=rabbitmq_config['dead_letter_queue'], durable=True)
channel.queue_bind(
    exchange=rabbitmq_config['dead_letter_exchange'],
    queue=rabbitmq_config['dead_letter_queue'],
    routing_key=rabbitmq_config['dead_letter_routing_key']
)

# Declare the main queue with dead-letter exchange arguments
channel.queue_declare(
    queue=rabbitmq_config['queue'],
    durable=True,
    arguments={
        'x-dead-letter-exchange': rabbitmq_config['dead_letter_exchange'],
        'x-dead-letter-routing-key': rabbitmq_config['dead_letter_routing_key']
    }
)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=rabbitmq_config['queue'], on_message_callback=on_message)

try:
    print("Starting consumer. Press CTRL+C to exit.")
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
