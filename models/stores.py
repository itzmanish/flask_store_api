from db import db


class StoreModel(db.Model):
    """
    Store Model
    """

    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    items = db.relationship("ItemModel", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
