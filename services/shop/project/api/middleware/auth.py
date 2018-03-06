from functools import wraps

import jwt
from flask import request, jsonify
from flask_api import status

from project.models.user import UserRole
from project.store import user_store
from project.utils.jwt import decode_auth_token


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            return jsonify({'status': 'fail', 'message': 'Authorization header missing.'}), status.HTTP_401_UNAUTHORIZED

        import re
        m = re.search('^Bearer (?P<token>.*)', authorization_header)

        if m is None:
            return jsonify({'status': 'fail', 'message': 'Invalid authorization header.'}), status.HTTP_400_BAD_REQUEST

        auth_token = m.group('token')

        try:
            user_id = decode_auth_token(auth_token)
        except jwt.ExpiredSignatureError:
            return jsonify({'status': 'fail', 'message': 'Expired token.'}), status.HTTP_401_UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({'status': 'fail', 'message': 'Invalid token.'}), status.HTTP_401_UNAUTHORIZED

        user = user_store.get(user_id)

        if user is None:
            return jsonify({'status': 'fail', 'message': 'Invalid user id.'}), status.HTTP_401_UNAUTHORIZED

        if not user.active:
            return jsonify({'status': 'fail', 'message': 'User is not active.'}), status.HTTP_403_FORBIDDEN

        return f(user_id, *args, **kwargs)

    return decorated_function


def check_admin_or_worker(f):
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        if user_store.get(user_id).role != UserRole.ADMIN and user_store.get(user_id).role != UserRole.WORKER:
            return jsonify({
                'status': 'fail',
                'message': 'You do not have permission to do that.'
            }), status.HTTP_403_FORBIDDEN
        return f(user_id, *args, **kwargs)

    return decorated_function
