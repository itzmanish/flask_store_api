from db import db
from requests import Response
from flask import url_for, request
from libs.mailgun import Mailgun


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

        subject = "Registration Confirmation.",
        text = f'Please click the link to confirm your registration: {link}'
        html = f'<html>Please click the link to confirm your registration: <a href="{link}">{link}</a></html>'

        return Mailgun.send_mail([self.email], subject, text, html)
