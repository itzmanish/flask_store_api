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
        try:
            row = ItemModel.find_by_name(name)
        except:
            return pretty_string('error on getting data from database', 500)

        if row:
            return row.json(), 200
        return pretty_string('no item found.', 404)

    # POST method

    def post(self, name):
        request_data = self.parser.parse_args()
        try:
            if ItemModel.find_by_name(name):
                return pretty_string('item already exists', 409)
        except:
            return pretty_string('error on getting data from database', 500)

        item = ItemModel(name, request_data['price'])
        item.add_item()
        return item.json(), 201

    # DELETE method
    def delete(self, name):
        try:
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_item()
                return '{} deleted'.format(name)
        except:
            return pretty_string('error on interacting database', 500)

        return pretty_string('items is already not exists.', 404)

    # PUT method

    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.add_item()
            except:
                return pretty_string('An error occured when adding items to database', 500), 500
        else:
            try:
                item.updated_item()
            except:
                return pretty_string('An error occured when updating items to database', 500), 500
        return updated_item.json()


class ItemsList(Resource):
    """
    Resource for class ItemsList
    """

    # GET request
    def get(self):
        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()

        insert_query = 'SELECT * FROM items'
        items = cursor.execute(insert_query)
        connection.commit()
        data = []
        for row in items:
            data.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': data}
