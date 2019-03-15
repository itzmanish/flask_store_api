from typing import List
from requests import Response, post


class Mailgun:

    MAILGUN_DOMAIN = 'sandbox5b12ae94a3254e47beb168cf0ef315d7.mailgun.org'
    MAILGUN_API_KEY = '39fcac254b8362b9e54ec4a41e56c3e7-de7062c6-96796fb6'
    FROM_TITLE = 'Store REST API'
    FROM_EMAIL = 'rudra@sandbox5b12ae94a3254e47beb168cf0ef315d7.mailgun.org'

    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        return post(
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
