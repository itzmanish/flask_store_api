import sqlite3
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    jwt_refresh_token_required,
)
from utils import pretty_string
from models.items import ItemModel


class Items(Resource):
    """
    New resource for Item class
    """

    # Argument Parser
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="Price field is not valid."
    )
    parser.add_argument(
        "store_id",
        type=int,
        required=True,
        help="Store id required to put items on specific store.",
    )

    # GET method
    @jwt_required  # protect route with authorization
    def get(self, name):
        # get items from database
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return pretty_string("no item found.", 404)

    # POST method
    @jwt_refresh_token_required
    def post(self, name):
        request_data = self.parser.parse_args()

        if ItemModel.find_by_name(name):
            return pretty_string("item already exists", 409)

        item = ItemModel(name, **request_data)
        try:
            item.save_to_db()
        except:
            return pretty_string("error on interacting database", 500)

        return item.json(), 201

    # DELETE method
    @jwt_refresh_token_required
    def delete(self, name):
        if get_jwt_claims():
            return {"msg": "Admin Priviliges required!"}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return "{} deleted".format(name)

        return pretty_string("items is already not exists.", 404)

    # PUT method
    @jwt_required
    def put(self, name):
        data = Items.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()


class ItemsList(Resource):
    """
    Resource for class ItemsList
    """

    # GET request
    @jwt_optional
    def get(self):
        items = list(map(lambda x: x.json(), ItemModel.query.all()))
        user = get_jwt_identity()
        if user:
            return {"items": items}
        # or this can be done simply with [x.json for x in ItemModel.query.all()]
        return {
            "items": [item["name"] for item in items],
            "message": "Please login to get more info about items.",
        }
