import sqlite3


class ItemModel:

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'

        data = cursor.execute(query, (name,))
        row = data.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def add_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'

        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'

        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

    def delete_item(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'

        cursor.execute(query, (self.name,))
        connection.commit()
        connection.close()
