from uuid import uuid4
from random import randint
from time import time

from db import db

CONFIRMATION_EMAIL_EXIPIRATION_DELTA = 1800
CONFIRMATION_PHONE_EXIPIRATION_DELTA = 300


class ConfirmationModel(db.Model):

    __tablename__ = "confirmation"

    id = db.Column(db.String(80), primary_key=True)
    otp = db.Column(db.String(8), nullable=True)
    email_expire_at = db.Column(db.Integer, nullable=False)
    otp_expire_at = db.Column(db.Integer, nullable=True)
    email_confirmed = db.Column(db.Boolean, nullable=False)
    phone_confirmed = db.Column(db.Boolean, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('UserModel')

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.email_confirmed = False
        self.user_confirmed = False
        self.id = str(uuid4())
        self.email_expire_at = int(
            time()) + CONFIRMATION_EMAIL_EXIPIRATION_DELTA

    @classmethod
    def find_by_id(cls, _id: str) -> 'ConfirmationModel':
        return cls.query.filter_by(id=_id).first()

    def gen_otp(self):
        range_start = 10**5
        range_end = (10**6)-1

        self.otp = str(randint(range_start, range_end))
        self.otp_expire_at = int(time()) + CONFIRMATION_PHONE_EXIPIRATION_DELTA
        return self.otp

    def verify_otp(self, otp):
        if self.otp == str(otp):
            return True
        return False

    @property
    def email_expired(self) -> bool:
        return time() > self.email_expire_at

    @property
    def otp_expired(self) -> bool:
        return time() > self.otp_expire_at

    def email_force_to_expire(self) -> None:
        if not self.email_expired:
            self.email_expire_at = int(time())
            self.save_to_db()

    def otp_force_to_expire(self) -> None:
        if not self.otp_expired:
            self.otp_expire_at = int(time())
            self.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
