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
        try:
            if data['username'] and data['password']:
                # Check for user already exist or not
                if UserModel.find_by_username(data['username']):
                    return pretty_string('User already exist.', 409), 409

                data['password'] = security.generate_password(
                    data['password'])
                connection = sqlite3.connect('data.db')
                cursor = connection.cursor()
                insert_query = 'INSERT INTO users VALUES (NULL, ?, ?)'
                cursor.execute(
                    insert_query, (data['username'], data['password']))
                connection.commit()
                connection.close()
                return pretty_string('user created successfully.', 201), 201
        except KeyError:
            return pretty_string('Please fill username and password field both', 409), 409
