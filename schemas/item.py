from ma import ma
from models.items import ItemModel
from models.stores import StoreModel


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = ItemModel
        load_only = ('store',)
        dump_only = ('id')
        include_fk = True
