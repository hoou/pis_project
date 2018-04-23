from typing import Dict

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from project.api import api
from project.api.errors import NotFound, BadRequest, InvalidPayload
from project.api.middleware.auth import active_required_if_logged_in
from project.business import users
from project.models.serializers import user as user_serial
from project.models.user import Country

ns = api.namespace('users')


@ns.route('/<int:user_resource_id>')
class UserItem(Resource):
    @jwt_required
    @active_required_if_logged_in
    @api.marshal_with(user_serial)
    def get(self, user_resource_id):
        user_to_get = users.get(user_resource_id)

        if user_to_get is None:
            raise NotFound('User not found.')

        user_id = get_jwt_identity()

        if user_to_get.id != user_id:
            raise BadRequest('You cannot get user profile of other person.')

        return user_to_get

    @jwt_required
    @active_required_if_logged_in
    def patch(self, user_resource_id):
        user_to_edit = users.get(user_resource_id)

        if user_to_edit is None:
            raise NotFound('User not found.')

        user_id = get_jwt_identity()

        if user_to_edit.id != user_id:
            raise BadRequest('You cannot edit profile of other person.')

        data: Dict = request.get_json()

        if data is None:
            raise InvalidPayload

        attributes = {'first_name', 'last_name', 'phone', 'street', 'zip_code', 'city', 'country', 'date_of_birth'}

        if not any(attribute in data for attribute in attributes):
            raise InvalidPayload

        country = data.get('country')
        if country is not None:
            try:
                data['country'] = Country(country)
            except ValueError as e:
                raise BadRequest(str(e))

        try:
            users.update(user_to_edit, attributes, data)
        except (TypeError, ValueError) as e:
            raise BadRequest(str(e))

        return {'message': 'Profile successfully modified.'}
