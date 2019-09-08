
from core import db


class ItemModel(db.Model):
    """
    Item Model
    """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), nullable=False, unique=True)
    test = db.Column(db.String(10), nullable=True)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey(
        "stores.id"), nullable=False)

    store = db.relationship("StoreModel")

    @classmethod
    def find_by_name(cls, name: str) -> "ItemModel":
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_item(self):
        db.session.delete(self)
        db.session.commit()
