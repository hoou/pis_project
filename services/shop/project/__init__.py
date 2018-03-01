from os import getenv

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


def create_app(script_info=None):
    # init app
    app = Flask(__name__)

    # set config
    app_settings = getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from .api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
