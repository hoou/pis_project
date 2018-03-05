import os

from flask import current_app


def test_app_is_development(app_dev):
    assert app_dev.config['SECRET_KEY'] == os.environ.get('SECRET_KEY')
    assert current_app is not None
    assert app_dev.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')
    assert app_dev.config['BCRYPT_LOG_ROUNDS'] == 4
    assert app_dev.config['TOKEN_EXPIRATION_DAYS'] == 30
    assert app_dev.config['TOKEN_EXPIRATION_SECONDS'] == 0


def test_app_is_testing(app):
    assert app.config['SECRET_KEY'] == os.environ.get('SECRET_KEY')
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')
    assert app.config['BCRYPT_LOG_ROUNDS'] == 4
    assert app.config['TOKEN_EXPIRATION_DAYS'] == 0
    assert app.config['TOKEN_EXPIRATION_SECONDS'] == 3


def test_app_is_production(app_prod):
    assert app_prod.config['SECRET_KEY'] == os.environ.get('SECRET_KEY')
    assert not app_prod.config['TESTING']
    assert app_prod.config['BCRYPT_LOG_ROUNDS'] == 13
    assert app_prod.config['TOKEN_EXPIRATION_DAYS'] == 30
    assert app_prod.config['TOKEN_EXPIRATION_SECONDS'] == 0
