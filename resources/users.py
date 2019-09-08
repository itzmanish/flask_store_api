import traceback

from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash

import core.utils as response_string
from core import BLACKLIST, pretty_string
from core.libs import MailGunException
from models.confirmation import ConfirmationModel
from models.users import UserModel
from schemas.confirmation import ConfirmationSchema
from schemas.user import UserPhoneSchema, UserSchema

user_schema = UserSchema()
confirmation_schema = ConfirmationSchema()
user_phone_schema = UserPhoneSchema()


class UserRegister(Resource):
    """
    Resource for class Authentication
    """
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        # Check for user already exist or not
        if UserModel.find_by_username(user.username):
            return pretty_string(response_string.USER_EXIST), 409

        user.password = generate_password_hash(
            user.password, method="pbkdf2:sha256", salt_length=10
        )
        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_mail()
            return pretty_string(USER_CREATED), 201

        except MailGunException as error:
            user.delete_from_db()
            return pretty_string(str(error)), 500

        except:
            traceback.print_exc()
            user.delete_from_db()
            return pretty_string(response_string.USER_FAILED_TO_CREATE), 500


class PhoneOTP(Resource):
    """
    Resource for Phone no. verification for user
    """
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        data = user_phone_schema.load(request.get_json())
        if user is not None:
            user.send_otp(**data)

        return pretty_string(response_string.OTP_SENT), 200


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return pretty_string(response_string.USER_NOT_FOUND), 404
        return user_schema.dump(user)

    @classmethod
    def post(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.make_admin()
            return pretty_string(response_string.USER_GRANTED_ADMIN)
        return pretty_string(response_string.USER_NOT_FOUND), 404

    @classmethod
    @jwt_refresh_token_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return pretty_string(response_string.USER_DELETED), 200
        return pretty_string(response_string.USER_NOT_FOUND), 404


class UserLogin(Resource):

    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=('email',))

        user = UserModel.find_by_username(user_data.username)
        if user and check_password_hash(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.email_confirmed:
                access_token = create_access_token(
                    identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            return pretty_string(response_string.USER_ACTIVATION_LINK_SENT)
        return pretty_string(response_string.INVALID_CREDENTIALS), 401


class UserLogout(Resource):

    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is unique id for jwt tokens
        BLACKLIST.add(jti)
        return pretty_string(response_string.USER_LOGGED_OUT)


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

        return pretty_string(response_string.INVALID_CREDENTIALS), 401
