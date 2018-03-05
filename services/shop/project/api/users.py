from flask import Blueprint, jsonify, request
from flask_api import status

from project.models.schemas import user_schema
from project.store import user_store
from project.store.user_store import DuplicateEmailError

users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    email = post_data.get('email')
    password = post_data.get('password')

    if email is None or password is None:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    try:
        user_store.add(email=email, password=password)
    except DuplicateEmailError:
        return jsonify({
            'status': 'fail',
            'message': 'Sorry. User with that email already exists.'
        }), status.HTTP_409_CONFLICT

    return jsonify({'status': 'success', 'message': 'User was added.'}), status.HTTP_201_CREATED


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'status': 'fail', 'message': 'User id must be int.'}), status.HTTP_400_BAD_REQUEST

    user = user_store.get(user_id)

    if user is None:
        return jsonify({'status': 'fail', 'message': 'User not found.'}), status.HTTP_404_NOT_FOUND

    return jsonify({
        'status': 'success',
        'data': user_schema.dump(user).data
    })


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = user_store.get_all()
    return jsonify({
        'status': 'success',
        'data': [user_schema.dump(user).data for user in users]
    })
