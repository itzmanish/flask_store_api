import sqlite3


def create_table():
    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()

    # create_table = 'CREATE TABLE IF NOT EXIST users (id INTEGER PRIMARY KEY, username text, password text)'
    create_table = 'CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)'
    cursor.execute(create_table)

    connection.commit()
    connection.close()


def insert_query(user):
    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()
    insert_query = 'INSERT INTO users VALUES (NULL, ?, ?)'
    cursor.execute(insert_query, (user['username'], user['password']))
    connection.commit()
    connection.close()


def get_all():
    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()

    insert_query = 'SELECT * from users'
    users = cursor.execute(insert_query)
    connection.commit()
    data = users.fetchall()
    connection.close()
    return data
