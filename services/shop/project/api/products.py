import ntpath
import os
import pathlib

import time
from flask import Blueprint, jsonify, request, current_app
from flask_api import status
from werkzeug.utils import secure_filename

from project.api.middleware.auth import authenticate, check_admin_or_worker
from project.models.schemas import product_schema, product_image_schema
from project.store import product_store
from project.utils.file import is_uploaded_file_allowed

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


@products_blueprint.route('/products/<product_id>/images', methods=['POST'])
@authenticate
@check_admin_or_worker
def add_product_image(user_id, product_id):
    product = product_store.get(product_id)

    if product is None:
        return jsonify({'status': 'fail', 'message': 'Product not found.'}), status.HTTP_404_NOT_FOUND

    file = request.files.get('file')

    if file is None:
        return jsonify({'status': 'fail', 'message': 'Invalid payload.'}), status.HTTP_400_BAD_REQUEST

    if not is_uploaded_file_allowed(file.filename):
        return jsonify({'status': 'fail', 'message': 'File extension not allowed.'}), status.HTTP_400_BAD_REQUEST

    basedir = os.path.abspath(os.path.dirname(__file__))

    product_dir = os.path.join(basedir, '..', current_app.config.get('UPLOAD_FOLDER'), product_id)

    pathlib.Path(product_dir).mkdir(parents=True, exist_ok=True)

    current_timestamp = int(time.time())
    secured_filename = secure_filename(ntpath.basename(file.filename))
    filename = f'{current_timestamp}_{secured_filename}'
    file_path = os.path.join(product_dir, filename)
    file.save(file_path)

    product_store.add_image(product, url=file_path)

    return jsonify({'status': 'success', 'message': 'Image was successfully uploaded.'}), status.HTTP_201_CREATED


@products_blueprint.route('/products/<product_id>/images', methods=['GET'])
def get_product_images(product_id):
    images = product_store.get_images(product_id)

    return jsonify({
        'status': 'success',
        'data': [product_image_schema.dump(image).data for image in images]
    })


@products_blueprint.route('/products/<product_id>/images/<image_id>', methods=['DELETE'])
@authenticate
@check_admin_or_worker
def delete_product_image(user_id, product_id, image_id):
    if not product_store.has_image(product_id, image_id):
        return jsonify({'status': 'fail', 'message': 'Image not found.'}), status.HTTP_404_NOT_FOUND

    product_store.delete_image(image_id)

    return jsonify({
        'status': 'success',
        'message': 'Image was successfully deleted.'
    })

