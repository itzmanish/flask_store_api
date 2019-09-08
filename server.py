# importing neccessary library
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Resource, Api
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager

from resources.users import (UserRegister,
                             User,
                             UserLogin,
                             TokenRefresh,
                             UserLogout,
                             PhoneOTP,
                             )
from resources.items import ItemsList, Items
from resources.stores import StoreList, Stores
from resources.confirmation import EmailConfirmation, ConfirmationByUser, PhoneConfirmation
from models.users import UserModel
from app import create_app
from core import BLACKLIST

load_dotenv('.env')

config_name = os.environ.get('ENV')
app = create_app(config_name)
jwt = JWTManager(app)

# @app.before_first_request
# def create_table():
#     db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@jwt.expired_token_loader
def expired_token_callback():
    return (
        jsonify({"description": "The token has expired.",
                 "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"description": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "unauthorised_token",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return (
        jsonify(
            {"description": "The token is not fresh.",
                "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST

# add claims for superuser
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    # returning opposite of is_admin value
    if user.is_admin:
        return False  # little bit workarround for further simplicity in resources
    return True


api = Api(app)

# route resource and register custom resource to Resource
@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    return {'Message': 'Welcome to store rest api v1.0. Please go through README for available routes on this api. ',
            'Link': 'https://github.com/itzmanish/flask_store_api/blob/advance/README.md'}, 200


api.add_resource(Items, "/item/<string:name>")

# route for retrieve Items
api.add_resource(ItemsList, "/items")

# route for store
api.add_resource(Stores, "/store/<string:name>")

# route to retrieve all stores
api.add_resource(StoreList, "/stores")


# authentication resource
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(User, "/users/<int:user_id>")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")
api.add_resource(PhoneOTP, '/send-otp')

api.add_resource(EmailConfirmation, '/confirmation/<string:confirmation_id>')
api.add_resource(PhoneConfirmation, '/verify-phone/<string:otp>')
api.add_resource(ConfirmationByUser, '/confirmation/user/<int:user_id>')

# run app with debug mode if env is development
if __name__ == "__main__":
    app.run(debug=True)
