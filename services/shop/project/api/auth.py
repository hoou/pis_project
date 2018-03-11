from flask import request
from flask_api import status
from flask_jwt_extended import create_access_token, jwt_required, create_refresh_token, jwt_refresh_token_required, \
    get_jwt_identity
from werkzeug.exceptions import Conflict
from flask_restplus import Resource

from project import bcrypt
from project.api import api
from project.api.errors import AuthenticationFailed, InvalidPayload, PermissionDenied
from project.api.middleware.auth import active_user
from project.business import users
from project.business.users import DuplicateEmailError

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
            users.add(email=email, password=password)
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

        user = users.get_by_email(email)

        if user is None:
            raise AuthenticationFailed

        if not user.active:
            raise PermissionDenied

        is_valid_password = bcrypt.check_password_hash(user.password, password)

        if not is_valid_password:
            raise AuthenticationFailed

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return {'message': 'User successfully logged in.', 'access_token': access_token, 'refresh_token': refresh_token}


@ns.route('/refresh')
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        user_id = get_jwt_identity()
        new_access_token = create_access_token(user_id)
        return {'message': 'Token successfully refreshed.', 'access_token': new_access_token}


@ns.route('/logout')
class UserLogout(Resource):
    @jwt_required
    @active_user
    def get(self):
        return {'message': 'User successfully logged out.'}
