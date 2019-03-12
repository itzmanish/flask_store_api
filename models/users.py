from typing import Dict, Union
from db import db

UserJSON = Dict[str, Union[int, str, bool]]


class UserModel(db.Model):
    """
    class for creating new user object.
    this should be in format of
    user(id, username, password)
    """

    # table and column initialized
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),  unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean())

    def __init__(self, username: str, password: str, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    def make_admin(self):
        self.is_admin = True
        db.session.add(self)
        db.session.commit()

    def json(self) -> UserJSON:
        return {'id': self.id, 'username': self.username, 'is_admin': self.is_admin}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()
