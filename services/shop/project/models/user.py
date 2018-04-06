import datetime
import re
from enum import IntEnum

from flask import current_app

from project import bcrypt, db
from project.models.product_rating import ProductRating
from project.models.order import Order


class UserRole(IntEnum):
    ADMIN = 0
    WORKER = 1
    CUSTOMER = 2


class Country(IntEnum):
    CZ = 0
    SK = 1


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _email = db.Column(db.String(64), nullable=False, unique=True)
    _password = db.Column(db.String(255), nullable=False)
    _active = db.Column(db.Boolean, nullable=False, default=False)
    _role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    _first_name = db.Column(db.String(64))
    _last_name = db.Column(db.String(64))
    _phone = db.Column(db.String(13))
    _street = db.Column(db.String(64))
    _zip_code = db.Column(db.String(5))
    _city = db.Column(db.String(64))
    _country = db.Column(db.Enum(Country))
    _date_of_birth = db.Column(db.Date())
    ratings = db.relationship('ProductRating', backref='user')
    orders = db.relationship('Order', backref='user', lazy=True)

    def __init__(self, email, password, first_name=None, last_name=None, phone=None, street=None, zip_code=None,
                 city=None, country=None, date_of_birth=None):

        self._set_email(email)
        self._set_password(password)

        self.active = False
        self.role = UserRole.CUSTOMER

        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.street = street
        self.zip_code = zip_code
        self.city = city
        self.country = country
        self.date_of_birth = date_of_birth

    def _set_email(self, value):
        if not isinstance(value, str):
            raise TypeError('Email must be string.')

        # http://emailregex.com/
        m = re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', value)
        if m is None:
            raise ValueError('Invalid email format.')

        self._email = value

    def _set_password(self, value):
        if not isinstance(value, str):
            raise TypeError('Password must be string.')

        m = re.match(r'^[a-zA-Z]\w{3,14}$', value)
        if m is None:
            raise ValueError(
                'Password must have between 4 and 15 chars, '
                'it must start with letter '
                'and can only be used letters, numbers and underscore.'
            )

        self._password = bcrypt.generate_password_hash(value, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()

    @property
    def id(self):
        return self._id

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        if not isinstance(value, bool):
            raise TypeError('Active flag must be boolean.')

        self._active = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, UserRole):
            values = [str(member.value) for name, member in UserRole.__members__.items()]
            raise TypeError('Role must be integer value from this set: ' + ", ".join(values))

        self._role = value

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if value is None:
            self._first_name = None
            return

        if not isinstance(value, str):
            raise TypeError('First name must be string.')

        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if value is None:
            self._last_name = None
            return

        if not isinstance(value, str):
            raise TypeError('Last name must be string.')

        self._last_name = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if value is None:
            self._phone = None
            return

        if not isinstance(value, str):
            raise TypeError('Phone must be string.')

        m = re.match(r'^\+(421|420)\d{9}$', value)
        if m is None:
            raise ValueError('Phone must have format \'+421ddddddddd\' or \'+420ddddddddd\', where \'d\' is number.')

        self._phone = value

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, value):
        if value is None:
            self._street = None
            return

        if not isinstance(value, str):
            raise TypeError('Street must be string.')

        self._street = value

    @property
    def zip_code(self):
        return self._zip_code

    @zip_code.setter
    def zip_code(self, value):
        if value is None:
            self._zip_code = None
            return

        if not isinstance(value, str):
            raise TypeError('ZIP code must be string.')

        m = re.match(r'^\d{5}$', value)
        if m is None:
            raise ValueError('ZIP code must contain 5 numbers.')

        self._zip_code = value

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        if value is None:
            self._city = None
            return

        if not isinstance(value, str):
            raise TypeError('City must be string.')

        self._city = value

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        if value is None:
            self._country = None
            return

        if not isinstance(value, Country):
            values = [str(member.value) for name, member in Country.__members__.items()]
            raise TypeError('Country must be integer value from this set: ' + ", ".join(values))

        self._country = value

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if value is None:
            self._date_of_birth = None
            return

        if not isinstance(value, datetime.date):
            raise TypeError('Date of birth must be date.')

        self._date_of_birth = value
