import logging
import os

from flask import Flask, Blueprint
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

from project.api import api

# init extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(script_info=None):
    # init app
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    logs_dir = os.path.join(basedir, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    fh = logging.FileHandler(os.path.join(logs_dir, 'app.log'))
    app.logger.addHandler(fh)

    # enable CORS
    CORS(app)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # init API
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    from project.api.users import ns as users_ns
    api.add_namespace(users_ns)
    from project.api.auth import ns as auth_ns
    api.add_namespace(auth_ns)
    from project.api.products import ns as products_ns
    api.add_namespace(products_ns)
    from project.api.categories import ns as categories_ns
    api.add_namespace(categories_ns)
    app.register_blueprint(blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
