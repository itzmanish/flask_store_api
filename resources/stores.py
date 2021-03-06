from flask_restful import Resource
from marshmallow import ValidationError

import core.utils as response_string
from core import pretty_string
from models.stores import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Stores(Resource):
    """
    Store resource for crud in stores
    """

    # GET method
    @classmethod
    def get(cls, name):
        # get items from database
        store = StoreModel.find_by_name(name)
        if store:

            return store_schema.dump(store), 200
        return pretty_string(response_string.STORE_NOT_FOUND), 404

    # POST method

    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            return pretty_string(response_string.STORE_EXIST), 409

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return pretty_string(response_string.DATABASE_ERROR), 500

        return store_schema.dump(store), 201

    # DELETE method
    @classmethod
    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_item()
            return "{} deleted".format(name)

        return pretty_string(response_string.STORE_NOT_EXIST), 404


class StoreList(Resource):
    """
    for all store
    """

    @classmethod
    def get(cls):
        return {"stores": store_list_schema.dump(StoreModel.query.all())}
