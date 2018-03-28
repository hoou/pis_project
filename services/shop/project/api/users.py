from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from project.api import api
from project.api.errors import NotFound
from project.api.middleware.auth import active_required_if_logged_in, admin_or_worker
from project.models.serializers import user as user_serial
from project.business import users

ns = api.namespace('users')


@ns.route('/')
class UserCollection(Resource):
    @api.marshal_list_with(user_serial)
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def get(self):
        return users.get_all()


@ns.route('/<int:user_to_get_id>')
class UserItem(Resource):
    @api.marshal_with(user_serial)
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def get(self, user_to_get_id):
        user = users.get(user_to_get_id)

        if user is None:
            raise NotFound

        return user
