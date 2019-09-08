import os
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_restful import Api
from core import ma, db, BLACKLIST

# local import
from core.config import app_config


def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')
    # initalizing
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URI')
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config["PROPAGATE_EXCEPTIONS"] = True
    # app.config["JWT_BLACKLIST_ENABLED"] = True
    # app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
    # app.config['JWT_SECRET_KEY']
    app.secret_key = os.environ.get('SECRET_KEY')
    db.init_app(app)
    ma.init_app(app)

    migrate = Migrate(app, db)

    return app
