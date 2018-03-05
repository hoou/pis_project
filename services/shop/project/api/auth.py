import jwt
from flask import Blueprint, request, jsonify
from flask_api import status

from project import bcrypt
from project.store import user_store
from project.store.user_store import DuplicateEmailError
from project.utils.jwt import decode_auth_token
from project.utils.jwt import encode_auth_token

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()

    if not data:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    try:
        user_store.add(email=email, password=password)
    except DuplicateEmailError:
        return jsonify({'status': 'fail', 'message': 'User with this email already exists.'}), status.HTTP_409_CONFLICT

    return jsonify({
        'status': 'success',
        'message': 'Successfully registered.'
    }), status.HTTP_201_CREATED


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()

    if not data:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    email = data.get('email')
    password = data.get('password')

    if email is None or password is None:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    user = user_store.get_by_email(email)

    if user is None:
        return jsonify({
            'status': 'fail',
            'message': 'User with this email is not registered.'
        }), status.HTTP_404_NOT_FOUND

    is_valid_password = bcrypt.check_password_hash(user.password, password)

    if not is_valid_password:
        return jsonify({'status': 'fail', 'message': 'Invalid password.'}), status.HTTP_400_BAD_REQUEST

    auth_token = encode_auth_token(user.id)

    return jsonify({
        'status': 'success',
        'message': 'User successfully logged in.',
        'auth_token': auth_token.decode()
    }), status.HTTP_200_OK


@auth_blueprint.route('/auth/logout', methods=['GET'])
def logout_user():
    authorization_header = request.headers.get('Authorization')

    if authorization_header is None:
        return jsonify({'status': 'fail', 'message': 'User is not logged in.'}), status.HTTP_401_UNAUTHORIZED

    import re
    m = re.search('^Bearer (?P<token>.*)', authorization_header)

    if m is None:
        return jsonify({'status': 'fail', 'message': 'Invalid authorization header.'}), status.HTTP_400_BAD_REQUEST

    token = m.group('token')

    try:
        decode_auth_token(token)
    except jwt.ExpiredSignatureError:
        return jsonify({'status': 'fail', 'message': 'Expired token.'}), status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return jsonify({'status': 'fail', 'message': 'Invalid token.'}), status.HTTP_401_UNAUTHORIZED

    return jsonify({'status': 'success', 'message': 'User successfully logged out.'}), status.HTTP_200_OK
