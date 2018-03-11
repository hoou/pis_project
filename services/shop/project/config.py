import os

import datetime


class BaseConfig:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    BCRYPT_LOG_ROUNDS = 13
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    UPLOAD_ALLOWED_EXT = {'jpg', 'jpeg'}


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=3)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=30)


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
