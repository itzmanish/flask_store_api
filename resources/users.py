import sqlite3
from flask_restful import Resource
from flask import request
from utils import pretty_string
from models.users import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from blacklist import BLACKLIST
from marshmallow import ValidationError
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    """
    Resource for class Authentication
    """
    @classmethod
    def post(cls):
        data = user_schema.load(request.get_json())

        # Check for user already exist or not
        if UserModel.find_by_username(data.username):
            return pretty_string("User already exist.", 409), 409

        data.password = generate_password_hash(
            data.password, method="pbkdf2:sha256", salt_length=10
        )

        data.save_to_db()

        return pretty_string("user created successfully.", 201), 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"msg": "User not found!"}, 404
        return user_schema.dump(user)

    @classmethod
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.make_admin()
            return {"msg": "successfully granted admin rights."}
        return {"msg": "No user exist with this user id."}, 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {"msg": "User has been successfully deleted!"}, 200
        return {"msg": "No user exist with this user id !"}, 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json())

        user = UserModel.find_by_username(user_data.username)
        if user and check_password_hash(user.password, user_data.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        return {"msg": "Invalid credential !"}, 401


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is unique id for jwt tokens
        BLACKLIST.add(jti)
        return {"message": "user successfully logged out!"}


class TokenRefresh(Resource):

    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        try:
            data = request.get_json()
            user_id = get_jwt_identity()
            user = UserModel.find_by_id(user_id)
            if user and check_password_hash(user.password, data['password']):
                new_token = create_access_token(user.id, fresh=False)
                return {"access_token": new_token}

        except KeyError:
            return {'message': 'Password field is required'}, 400

        return {"message": "Wrong password"}, 401
