from functools import wraps

import jwt
from flask import request

from project.api.errors import *
from project.models.user import UserRole
from project.store import user_store
from project.utils.jwt import decode_auth_token


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get('Authorization')

        if authorization_header is None:
            raise PermissionDenied

        import re
        m = re.search('^Bearer (?P<token>.*)', authorization_header)

        if m is None:
            raise ParseError

        auth_token = m.group('token')

        try:
            user_id = decode_auth_token(auth_token)
        except jwt.ExpiredSignatureError:
            raise ExpiredAccessToken
        except jwt.InvalidTokenError:
            raise InvalidAccessToken

        user = user_store.get(user_id)

        if user is None:
            raise AuthenticationFailed

        if not user.active:
            raise PermissionDenied

        return f(user_id, *args, **kwargs)

    return decorated_function


def check_admin_or_worker(f):
    @wraps(f)
    def decorated_function(user_id, *args, **kwargs):
        if user_store.get(user_id).role != UserRole.ADMIN and user_store.get(user_id).role != UserRole.WORKER:
            raise PermissionDenied
        return f(user_id, *args, **kwargs)

    return decorated_function
