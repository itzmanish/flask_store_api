import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from utils import pretty_string
from models.items import ItemModel


class Items(Resource):
    """
    New resource for Item class
    """

    # Argument Parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='Price field is not valid.'
                        )

    # GET method
    @jwt_required()  # protect route with authorization
    def get(self, name):
        # get items from database
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return pretty_string('no item found.', 404)

    # POST method

    def post(self, name):
        request_data = self.parser.parse_args()

        if ItemModel.find_by_name(name):
            return pretty_string('item already exists', 409)

        item = ItemModel(name, request_data['price'])
        try:
            item.save_to_db()
        except:
            return pretty_string('error on interacting database', 500)

        return item.json(), 201

    # DELETE method
    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return '{} deleted'.format(name)

        return pretty_string('items is already not exists.', 404)

    # PUT method

    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    """
    Resource for class ItemsList
    """

    # GET request
    def get(self):
        # or this can be done simply with [x.json for x in ItemModel.query.all()]
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
