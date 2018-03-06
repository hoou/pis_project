from flask import Blueprint, jsonify, request
from flask_api import status

from project.api.middleware.auth import authenticate, check_admin_or_worker
from project.models.schemas import product_schema
from project.store import product_store

products_blueprint = Blueprint('products', __name__)


@products_blueprint.route('/products', methods=['GET'])
def get_all_products():
    products = product_store.get_all()

    return jsonify({
        'status': 'success',
        'data': [product_schema.dump(product).data for product in products]
    })


@products_blueprint.route('/products/<product_id>', methods=['GET'])
def get_single_product(product_id):
    product = product_store.get(product_id)

    if product is None:
        return jsonify({'status': 'fail', 'message': 'Product not found.'}), status.HTTP_404_NOT_FOUND

    return jsonify({
        'status': 'success',
        'data': product_schema.dump(product).data
    })


@products_blueprint.route('/products', methods=['POST'])
@authenticate
@check_admin_or_worker
def add_product(user_id):
    data = request.get_json()

    if not data:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    name = data.get('name')
    price = data.get('price')
    description = data.get('description')

    if name is None or price is None:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    product_store.add(name=name, price=price, description=description)

    return jsonify({
        'status': 'success',
        'message': 'Product was successfully added.'
    }), status.HTTP_201_CREATED
