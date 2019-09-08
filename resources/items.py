import sqlite3
from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    jwt_refresh_token_required,
)

from marshmallow import ValidationError
import core.utils as response_string
from core import pretty_string
from models.items import ItemModel
from schemas.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Items(Resource):
    """
    New resource for Item class
    """

    # GET method
    @classmethod
    @jwt_required  # protect route with authorization
    def get(cls, name):
        # get items from database
        item = ItemModel.find_by_name(name)
        if item:

            return item_schema.dump(item), 200
        return pretty_string(response_string.ITEM_NOT_FOUND)

    # POST method
    @classmethod
    @jwt_refresh_token_required
    def post(cls, name):

        item_data = request.get_json()
        item_data['name'] = name

        if ItemModel.find_by_name(name):
            return pretty_string(response_string.ITEM_EXIST)
        item = item_schema.load(item_data)

        try:
            item.save_to_db()
        except:
            return pretty_string(response_string.DATABASE_ERROR)

        return item_schema.dump(item), 201

    # DELETE method
    @classmethod
    @jwt_refresh_token_required
    def delete(cls, name):
        if get_jwt_claims():
            return pretty_string(response_string.ADMIN_PERMISSION_ERROR), 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_item()
            return "{} deleted".format(name)

        return pretty_string(response_string.ITEM_NOT_EXIST)

    # PUT method
    @classmethod
    @jwt_required
    def put(cls, name):

        data = request.get_json()
        data['name'] = name
        item = ItemModel.find_by_name(name)
        if item is None:
            item = item_schema.load(data)
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()

        return item_schema.dump(item)


class ItemsList(Resource):
    """
    Resource for class ItemsList
    """

    # GET request
    @classmethod
    @jwt_optional
    def get(cls):

        items = item_list_schema.dump(ItemModel.query.all())
        user = get_jwt_identity()
        if user:
            return {"items": items}
        # or this can be done simply with [x.json for x in ItemModel.query.all()]
        return {
            "items": [item["name"] for item in items],
            "message": response_string.LOGIN_REQUIRED,
        }
