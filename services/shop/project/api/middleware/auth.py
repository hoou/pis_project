from functools import wraps

from flask_jwt_extended import get_jwt_identity

from project.api.errors import *
from project.business import users
from project.models.user import UserRole


def active_required_if_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_jwt_identity() is None:
            return f(*args, **kwargs)

        user = users.get(get_jwt_identity())
        if user is None:
            raise AuthenticationFailed

        if not user.active:
            raise PermissionDenied

        return f(*args, **kwargs)

    return decorated_function


def admin_or_worker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        if users.get(user_id).role != UserRole.ADMIN and users.get(user_id).role != UserRole.WORKER:
            raise PermissionDenied
        return f(*args, **kwargs)

    return decorated_function
