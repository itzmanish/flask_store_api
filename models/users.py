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
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean())

    def __init__(self, username: str, password: str, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin

    @classmethod
    def make_admin(cls):
        self.is_admin = True
        db.session.add(cls)
        db.session.commit()

    def json(self) -> UserJSON:
        return {"id": self.id, "username": self.username, "is_admin": self.is_admin}

    @classmethod
    def save_to_db(cls):
        db.session.add(cls)
        db.session.commit()

    @classmethod
    def delete_from_db(cls):
        db.session.delete(cls)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()
