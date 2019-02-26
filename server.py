# importing neccessary library
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
from db import create_table
from users import RegisterUser
from items import Items, ItemsList
# initalizing
app = Flask(__name__)
app.secret_key = 'Manish'
api = Api(app)
if not os.path.isfile('./data.db'):
    create_table()

# for auth
jwt = JWT(app, authenticate, identity)

# route resource and register custom resource to Resource
# this endpoint can be accessed at http://localhost:5000/students/"any name you can type here"
api.add_resource(Items, '/items/<string:name>')

# route for retrieve Items
api.add_resource(ItemsList, '/items')

# authentication resource
api.add_resource(RegisterUser, '/register')

# run app with debug mode if env is development
if __name__ == "__main__":
    app.run(debug=True)
