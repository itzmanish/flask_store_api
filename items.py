import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from utils import pretty_string


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
            row = self.find_by_item(name)
        except:
            return pretty_string('error on getting data from database', 500)

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        return pretty_string('no item found.', 404)

    # POST method

    def post(self, name):
        request_data = self.parser.parse_args()
        try:
            if self.find_by_item(name):
                return pretty_string('item already exists', 409)
        except:
            return pretty_string('error on getting data from database', 500)

        item = {'name': name, 'price': request_data['price']}
        self.add_item(item)
        return item, 201

    # DELETE method
    def delete(self, name):
        try:
            if self.find_by_item(name):
                self.delete_item(name)
                return '{} deleted'.format(name)
        except:
            return pretty_string('error on interacting database', 500)

        return pretty_string('items is already not exists.', 404)

    # PUT method

    def put(self, name):
        data = Items.parser.parse_args()
        item = self.find_by_item(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.add_item(updated_item)
            except:
                return pretty_string('An error occured when adding items to database', 500), 500
        else:
            try:
                self.update_item(updated_item)
            except:
                return pretty_string('An error occured when updating items to database', 500), 500
        return updated_item

    @classmethod
    def find_by_item(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'

        data = cursor.execute(query, (name,))
        row = data.fetchone()
        connection.close()
        return row

    def add_item(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'

        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    def update_item(self, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'

        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def delete_item(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'

        cursor.execute(query, (name,))
        connection.commit()
        connection.close()


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
