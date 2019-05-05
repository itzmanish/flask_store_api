# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from typing import List
from requests import Response, post
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

FAILED_LOADING_API_KEY = 'Failed to load SendGrid api key'
SENDING_FAILED = 'Error in sending confirmation mail, user registration failed'


class SendGridMailException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SendGridMail:

    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

    FROM_EMAIL = 'rudra@gmail.com'
    FROM_TITLE = 'Store Rest API'

    @classmethod
    def send_mail(cls, email: str, subject: str, text: str, html: str) -> Response:

        if cls.SENDGRID_API_KEY is None:
            raise SendGridMailException(FAILED_LOADING_API_KEY)

        try:
            response = post(
                f'https://api.sendgrid.com/v3/mail/send',
                headers={'Authorization': f'Bearer {cls.SENDGRID_API_KEY}',
                         'Content-Type': 'application/json'},
                data={
                    "personalizations":
                        [
                            {
                                "to": email,
                                "subject": subject
                            }
                        ],
                        "content": [
                            {
                                "type": "text/plain",
                                "value": text
                            }
                        ],
                        "from": {
                            "email": cls.FROM_EMAIL, "name": cls.FROM_TITLE
                        },
                },
            )

            if response.status_code != 202:
                raise SendGridMailException(SENDING_FAILED)

        except Exception as e:
            print(e)
            raise SendGridMailException(SENDING_FAILED)
