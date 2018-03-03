import os

from flask import current_app


def test_app_is_development(app_dev):
    assert app_dev.config['SECRET_KEY'] == 'my_precious'
    assert current_app is not None
    assert app_dev.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')


def test_app_is_testing(app):
    assert app.config['SECRET_KEY'] == 'my_precious'
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_TEST_URL')


def test_app_is_production(app_prod):
    assert app_prod.config['SECRET_KEY'] == 'my_precious'
    assert not app_prod.config['TESTING']
