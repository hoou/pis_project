from flask import request
from flask_api import status
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.exceptions import Conflict
from flask_restplus import Resource

from project import bcrypt
from project.api import api
from project.api.errors import AuthenticationFailed, InvalidPayload, PermissionDenied
from project.api.middleware.auth import active_user
from project.store import user_store
from project.store.user_store import DuplicateEmailError

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

        # auth_token = encode_auth_token(user.id)
        access_token = create_access_token(user.id)

        return {'message': 'User successfully logged in.', 'access_token': access_token}


@ns.route('/logout')
class UserLogout(Resource):
    @jwt_required
    @active_user
    def get(self):
        return {'message': 'User successfully logged out.'}
