# importing neccessary library
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
from db import create_table
from resources.users import RegisterUser
from resources.items import Items, ItemsList
# initalizing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    from db import db
    db.init_app(app)
    app.run(debug=True)
