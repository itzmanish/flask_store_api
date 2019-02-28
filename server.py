# importing neccessary library
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.users import RegisterUser
from resources.items import Items, ItemsList
from resources.stores import StoreList, Stores
# initalizing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'Manish'
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()


# for auth
jwt = JWT(app, authenticate, identity)

# route resource and register custom resource to Resource
# this endpoint can be accessed at http://localhost:5000/students/"any name you can type here"
api.add_resource(Items, '/item/<string:name>')

# route for retrieve Items
api.add_resource(ItemsList, '/items')

# route for store
api.add_resource(Stores, '/store/<string:name>')

# route to retrieve all stores
api.add_resource(StoreList, '/stores')

# authentication resource
api.add_resource(RegisterUser, '/register')

# run app with debug mode if env is development
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
