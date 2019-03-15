from db import db
from requests import Response, post
from flask import url_for, request

MAILGUN_DOMAIN = 'sandbox5b12ae94a3254e47beb168cf0ef315d7.mailgun.org'
MAILGUN_API_KEY = '39fcac254b8362b9e54ec4a41e56c3e7-de7062c6-96796fb6'
FROM_TITLE = 'Store REST API'
FROM_EMAIL = 'rudra@sandbox5b12ae94a3254e47beb168cf0ef315d7.mailgun.org'


class UserModel(db.Model):
    """
    class for creating new user object.
    this should be in format of
    user(id, username, password)
    """

    # table and column initialized
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False, unique=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    active = db.Column(db.Boolean(), default=False)

    def make_admin(self):
        self.is_admin = True
        db.session.add(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_mail(self) -> Response:
        link = request.url_root[0:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f'{FROM_TITLE} <{FROM_EMAIL}>',
                "to": self.email,
                "subject": "Registration Confirmation.",
                "text": f'Please click the link to confirm your registration {link}'
            },
        )
