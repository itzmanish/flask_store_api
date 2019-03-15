import traceback
from flask_restful import Resource
from flask import request
from utils import *
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
            return pretty_string(USER_EXIST), 409

        data.password = generate_password_hash(
            data.password, method="pbkdf2:sha256", salt_length=10
        )
        try:
            data.save_to_db()
            data.send_confirmation_mail()
            return pretty_string(USER_CREATED), 201

        except:
            traceback.print_exc()
            return pretty_string(USER_FAILED_TO_CREATE), 500


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return pretty_string(USER_NOT_FOUND), 404
        return user_schema.dump(user)

    @classmethod
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.make_admin()
            return pretty_string(USER_GRANTED_ADMIN)
        return pretty_string(USER_NOT_FOUND), 404

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return pretty_string(USER_DELETED), 200
        return pretty_string(USER_NOT_FOUND), 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=('email',))

        user = UserModel.find_by_username(user_data.username)
        if user and check_password_hash(user.password, user_data.password):
            if user.active:
                access_token = create_access_token(
                    identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            return pretty_string(USER_ACTIVATION_LINK_SENT)
        return pretty_string(INVALID_CREDENTIALS), 401


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is unique id for jwt tokens
        BLACKLIST.add(jti)
        return pretty_string(USER_LOGGED_OUT)


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return pretty_string(USER_NOT_FOUND), 404
        user.active = True
        user.save_to_db()
        return pretty_string(USER_ACTIVATED)


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

        return pretty_string(INVALID_CREDENTIALS), 401
