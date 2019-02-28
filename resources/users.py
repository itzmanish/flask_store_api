import security
import sqlite3
from flask_restful import Resource, reqparse
from utils import pretty_string
from models.users import UserModel


class RegisterUser(Resource):
    """
    Resource for class Authentication
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='this field can\'t be blank'
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='this field can\'t be blank'
                        )

    def post(self):
        data = RegisterUser.parser.parse_args()
        if data['username'] and data['password']:
            # Check for user already exist or not
            if UserModel.find_by_username(data['username']):
                return pretty_string('User already exist.', 409), 409

            data['password'] = security.generate_password(
                data['password'])
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

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return {'msg': 'User has been successfully deleted!'}, 200
        return {'msg': 'No user exist with this user id !'}, 404
