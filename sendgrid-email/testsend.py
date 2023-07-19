import os
import sendgrid
from sendgrid.helpers.mail import *
import dotenv
import logging

dotenv.load_dotenv()

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# set up logging
logging.basicConfig(level=LOG_LEVEL)

FROM_EMAIL = os.environ.get('FROM_EMAIL')
FROM_NAME = os.environ.get('FROM_NAME')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

logging.info(f"FROM_EMAIL: {FROM_EMAIL}")
logging.info(f"FROM_NAME: {FROM_NAME}")
logging.info(f"SENDGRID_API_KEY: {SENDGRID_API_KEY}")

subject = "Hello World from the SendGrid Python Library!"
to_email = "mike@technomonk.com"
from_email = FROM_EMAIL

logging.info(f"Sending email to {to_email} with subject {subject}")

html_content = "<strong>Hello, Email!</strong>"
plain_text_content = "Hello, Email!"

sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
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
        },
        {
            "type": "text/plain",
            "value": plain_text_content
        }
    ]
}

logging.info(f"Sending email with data: {data}")

# make request to sendgrid API to send email with data payload and print response
try:
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.to_dict)




