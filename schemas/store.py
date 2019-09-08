from core import ma
from models.stores import StoreModel
from schemas.item import ItemSchema


class StoreSchema(ma.ModelSchema):

    items = ma.Nested(ItemSchema, many=True)

    class Meta:
        model = StoreModel
        dump_only = ('id',)
        include_fk = True
