from flask import request
from flask_api import status
from werkzeug.exceptions import Conflict
from flask_restplus import Resource

from project import bcrypt
from project.api import api
from project.api.errors import AuthenticationFailed, InvalidPayload, PermissionDenied
from project.api.middleware.auth import authenticate
from project.store import user_store
from project.store.user_store import DuplicateEmailError
from project.utils.jwt import encode_auth_token

ns = api.namespace('auth')


@ns.route('/register')
class UserRegistration(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            raise InvalidPayload

        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise InvalidPayload

        try:
            user_store.add(email=email, password=password)
        except DuplicateEmailError:
            raise Conflict('User with this email already exists.')

        return {'message': 'Successfully registered.'}, status.HTTP_201_CREATED


@ns.route('/login')
class UserLogin(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            raise InvalidPayload

        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            raise InvalidPayload

        user = user_store.get_by_email(email)

        if user is None:
            raise AuthenticationFailed

        if not user.active:
            raise PermissionDenied

        is_valid_password = bcrypt.check_password_hash(user.password, password)

        if not is_valid_password:
            raise AuthenticationFailed

        auth_token = encode_auth_token(user.id)

        return {'message': 'User successfully logged in.', 'auth_token': auth_token.decode()}


@ns.route('/logout')
class UserLogout(Resource):
    @authenticate
    def get(self, user_id):
        return {'message': 'User successfully logged out.'}
