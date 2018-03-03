from os import getenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import orm

# init db

db = SQLAlchemy()

session = orm.scoped_session(orm.sessionmaker())
session.configure(bind="engine")


def create_app(script_info=None):
    # init app
    app = Flask(__name__)

    # set config
    app_settings = getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # register blueprints
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})
    return app
