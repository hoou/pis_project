from functools import wraps

from flask_jwt_extended import get_jwt_identity, jwt_required

from project.api.errors import *
from project.models.user import UserRole
from project.store import user_store


def active_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = user_store.get(get_jwt_identity())
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
        if user_store.get(user_id).role != UserRole.ADMIN and user_store.get(user_id).role != UserRole.WORKER:
            raise PermissionDenied
        return f(*args, **kwargs)

    return decorated_function
