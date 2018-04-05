from enum import IntEnum

from flask import current_app

from project import bcrypt, db


class UserRole(IntEnum):
    ADMIN = 0
    WORKER = 1
    CUSTOMER = 2


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(13))
    street = db.Column(db.String(64))
    zip = db.Column(db.String(5))
    city = db.Column(db.String(64))
    country = db.Column(db.String(64))
    date_of_birth = db.Column(db.Date())
    ratings = db.relationship('ProductRating', backref='user')
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, email, password, first_name=None, last_name=None, phone=None, street=None, zip_code=None,
                 city=None, country=None, date_of_birth=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street = street
        self.zip = zip_code
        self.city = city
        self.country = country
        self.date_of_birth = date_of_birth
