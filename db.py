import sqlite3
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_table():
    connection = sqlite3.connect('data.db')

    cursor = connection.cursor()

    # create_table = 'CREATE TABLE IF NOT EXIST users (id INTEGER PRIMARY KEY, username text, password text)'
    create_table_user = 'CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)'
    create_table_items = 'CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price real)'
    cursor.execute(create_table_user)
    cursor.execute(create_table_items)

    connection.commit()
    connection.close()
