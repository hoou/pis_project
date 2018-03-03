from flask import Blueprint, jsonify, request
from flask_api import status
from project import db
from project.api.models import User
from project.api.schemas import user_schema
from sqlalchemy.exc import DataError, IntegrityError

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
        db.session.add(User(email=email, password=password))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(
            {'status': 'fail', 'message': 'Sorry. User with that email already exists.'}), status.HTTP_409_CONFLICT

    return jsonify({'status': 'success', 'message': 'User was added.'}), status.HTTP_201_CREATED


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    try:
        user = User.query.filter_by(id=user_id).first()
    except DataError:
        return jsonify({'status': 'fail', 'message': 'Bad request.'}), status.HTTP_400_BAD_REQUEST

    if user is None:
        return jsonify({'status': 'fail', 'message': 'User not found.'}), status.HTTP_404_NOT_FOUND

    return jsonify({
        'status': 'success',
        'data': user_schema.dump(user).data
    })


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.order_by(User.id).all()
    return jsonify({
        'status': 'success',
        'data': [user_schema.dump(user).data for user in users]
    })
