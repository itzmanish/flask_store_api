# importing neccessary library
import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from resources.users import (
    UserRegister,
    User,
    UserLogin,
    TokenRefresh,
    UserLogout,
)
from resources.items import Items, ItemsList
from resources.stores import StoreList, Stores
from models.users import UserModel
from blacklist import BLACKLIST

# initalizing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.secret_key = 'Manish'  # app.config['JWT_SECRET_KEY']
api = Api(app)

# for auth
jwt = JWTManager(app)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

# add claims for superuser
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    # returning opposite of is_admin value
    if user.is_admin:
        return False  # little bit workarround for further simplicity in resources
    return True


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'unauthorised_token'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


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
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

# run app with debug mode if env is development
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
