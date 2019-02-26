import sqlite3


class UserModel:
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
