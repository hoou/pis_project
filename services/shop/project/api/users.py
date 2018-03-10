from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from project.api import api
from project.api.errors import NotFound
from project.api.middleware.auth import active_user, admin_or_worker
from project.models.serializers import user as user_serial
from project.store import user_store

ns = api.namespace('users')


@ns.route('/')
class UserCollection(Resource):
    @api.marshal_list_with(user_serial)
    @jwt_required
    @active_user
    @admin_or_worker
    def get(self):
        return user_store.get_all()


@ns.route('/<int:user_to_get_id>')
class UserItem(Resource):
    @api.marshal_with(user_serial)
    @jwt_required
    @active_user
    @admin_or_worker
    def get(self, user_to_get_id):
        user = user_store.get(user_to_get_id)

        if user is None:
            raise NotFound

        return user
