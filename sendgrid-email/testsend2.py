import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import dotenv

dotenv.load_dotenv()

message = Mail(
    from_email='darkflib@wwff.tech',
    to_emails='mike@technomonk.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sendgrid_client = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sendgrid_client.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e)