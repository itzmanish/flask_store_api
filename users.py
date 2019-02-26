import security
import sqlite3
from flask_restful import Resource, reqparse
from utils import pretty_string


class User:
    """
    class for creating new user object. 
    this should be in format of
    user(id, username, password)
    """

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conncetion = sqlite3.connect('data.db')
        cursor = conncetion.cursor()

        query = 'SELECT * FROM users WHERE username=?'

        results = cursor.execute(query, (username,))

        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conncetion.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conncetion = sqlite3.connect('data.db')
        cursor = conncetion.cursor()

        query = 'SELECT * FROM users WHERE id=?'

        results = cursor.execute(query, (_id,))

        row = results.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        conncetion.close()
        return user


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
                if User.find_by_username(data['username']):
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
