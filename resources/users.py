import sqlite3
from flask_restful import Resource, reqparse
from utils import pretty_string
from models.users import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='Username can\'t be blank'
                          )

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='Password can\'t be blank'
                          )


class UserRegister(Resource):
    """
    Resource for class Authentication
    """

    def post(self):
        data = _user_parser.parse_args()
        if data['username'] and data['password']:
            # Check for user already exist or not
            if UserModel.find_by_username(data['username']):
                return pretty_string('User already exist.', 409), 409

            data['password'] = generate_password_hash(
                data['password'], method='pbkdf2:sha256', salt_length=10)
            user = UserModel(**data)
            user.save_to_db()
            return pretty_string('user created successfully.', 201), 201
        return pretty_string('Please check username and password field again.', 404), 404


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        return {'msg': 'User not found!'}, 404

    def post(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.make_admin()
            return {'msg': 'successfully granted admin rights.'}
        return {'msg': 'No user exist with this user id.'}, 404

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'msg': 'User has been successfully deleted!'}, 200
        return {'msg': 'No user exist with this user id !'}, 404


class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'msg': 'Invalid credential !'}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user = get_jwt_identity()
        new_token = create_access_token(user, fresh=False)
        return {'access_token': new_token}
