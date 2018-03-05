import datetime

from flask import current_app
import jwt
from project import bcrypt, db


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(13))
    street = db.Column(db.String(64))
    zip = db.Column(db.String(5))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date())

    def __init__(self, email, password, first_name=None, last_name=None, phone=None, street=None, zip=None,
                 city=None, country=None, date_of_birth=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street = street
        self.zip = zip
        self.city = city
        self.country = country
        self.date_of_birth = date_of_birth

    def encode_auth_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
            ),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
        }

        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    @staticmethod
    def decode_auth_token(token):
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
