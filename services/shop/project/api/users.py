from flask import Blueprint, jsonify
from flask_api import status

from project.api.middleware.auth import authenticate, check_admin
from project.models.schemas import user_schema
from project.store import user_store

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/<user_to_find_id>', methods=['GET'])
@authenticate
@check_admin
def get_single_user(user_id, user_to_find_id):
    try:
        user_to_find_id = int(user_to_find_id)
    except ValueError:
        return jsonify({'status': 'fail', 'message': 'User id must be int.'}), status.HTTP_400_BAD_REQUEST

    user = user_store.get(user_to_find_id)

    if user is None:
        return jsonify({'status': 'fail', 'message': 'User not found.'}), status.HTTP_404_NOT_FOUND

    return jsonify({
        'status': 'success',
        'data': user_schema.dump(user).data
    })


@users_blueprint.route('/users', methods=['GET'])
@authenticate
@check_admin
def get_all_users(user_id):
    users = user_store.get_all()
    return jsonify({
        'status': 'success',
        'data': [user_schema.dump(user).data for user in users]
    })
