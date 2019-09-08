import os
from typing import List
from requests import Response, post


FAILED_LOADING_API_KEY = 'Failed to load Mailgun api key'
FAILED_LOADING_DOMAIN = 'Failed to load Mailgun domain'
SENDING_FAILED = 'Error in sending confirmation mail, user registrationn failed'


class MailGunException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Mailgun:

    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

    FROM_TITLE = 'Store REST API'
    FROM_EMAIL = 'rudra@sandbox5b12ae94a3254e47beb168cf0ef315d7.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:

        if cls.MAILGUN_API_KEY is None:
            raise MailGunException(FAILED_LOADING_API_KEY)

        if cls.MAILGUN_DOMAIN is None:
            raise MailGunException(FAILED_LOADING_DOMAIN)

        response = post(
            f'https://api.mailgun.net/v3/{cls.MAILGUN_DOMAIN}/messages',
            auth=("api", cls.MAILGUN_API_KEY),
            data={
                "from": f'{cls.FROM_TITLE} <{cls.FROM_EMAIL}>',
                "to": email,
                "subject": subject,
                "text": text,
                "html": html,
            },
        )

        if response.status_code != 200:
            raise MailGunException(SENDING_FAILED)
