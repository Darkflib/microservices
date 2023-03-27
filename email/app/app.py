from flask import Flask, request
from producer import publish_task
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/send-notification', methods=['POST'])
def send_notification():
    recipient = request.form['recipient']
    subject = 'Hello from Pika and RabbitMQ'
    context = {'name': request.form['name']}
    logging.info(f"Sending email to {recipient} with subject {subject}")
    publish_task(subject, recipient, 'email_template.html', context)
    return 'Email notification sent', 200

if __name__ == '__main__':
    app.run()

