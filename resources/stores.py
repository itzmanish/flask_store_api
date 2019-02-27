from flask_restful import Resource
from models.stores import StoreModel
from utils import pretty_string


class Stores(Resource):
    """
    Store resource for crud in stores
    """

    # GET method

    def get(self, name):
        # get items from database
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return pretty_string('store not found.', 404)

    # POST method

    def post(self, name):
        if StoreModel.find_by_name(name):
            return pretty_string('item already exists', 409)

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return pretty_string('error on interacting database', 500)

        return store.json(), 201

    # DELETE method
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_item()
            return '{} deleted'.format(name)

        return pretty_string('items is already not exists.', 404)


class StoreList(Resource):
    """
    for all store
    """

    def get(self):
        return {'stores': [x.json() for x in StoreModel.query.all()]}
