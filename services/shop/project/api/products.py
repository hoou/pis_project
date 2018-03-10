import ntpath
import os
import pathlib
import time

from flask import request, current_app
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from project.api import api
from project.api.errors import InvalidPayload, NotFound
from project.api.middleware.auth import active_user, admin_or_worker
from project.store import product_store
from project.utils.file import is_uploaded_file_allowed
from project.models.serializers import product as product_serial
from project.models.serializers import product_image as product_image_serial

ns = api.namespace('products')


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(product_serial)
    def get(self):
        return product_store.get_all()

    @jwt_required
    @active_user
    @admin_or_worker
    def post(self):
        data = request.get_json()

        if not data:
            raise InvalidPayload

        name = data.get('name')
        price = data.get('price')
        description = data.get('description')

        if name is None or price is None:
            raise InvalidPayload

        product_store.add(name=name, price=price, description=description)

        return {'message': 'Product was successfully added.'}, status.HTTP_201_CREATED


@ns.route('/<int:product_id>')
class ProductItem(Resource):
    @api.marshal_with(product_serial)
    def get(self, product_id):
        product = product_store.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        return product


@ns.route('/<int:product_id>/images')
class ProductImageCollection(Resource):
    @api.marshal_list_with(product_image_serial)
    def get(self, product_id):
        return product_store.get_images(product_id)

    @jwt_required
    @active_user
    @admin_or_worker
    def post(self, product_id):
        product = product_store.get(product_id)

        if product is None:
            return {'message': 'Product not found.'}, status.HTTP_404_NOT_FOUND

        file = request.files.get('file')

        if file is None:
            return {'message': 'Invalid payload.'}, status.HTTP_400_BAD_REQUEST

        if not is_uploaded_file_allowed(file.filename):
            return {'message': 'File extension not allowed.'}, status.HTTP_400_BAD_REQUEST

        # TODO move this shit to util function or something
        basedir = os.path.abspath(os.path.dirname(__file__))

        product_dir = os.path.join(basedir, '..', current_app.config.get('UPLOAD_FOLDER'), str(product_id))

        pathlib.Path(product_dir).mkdir(parents=True, exist_ok=True)

        current_timestamp = int(time.time())

        from werkzeug.utils import secure_filename
        secured_filename = secure_filename(ntpath.basename(file.filename))

        filename = f'{current_timestamp}_{secured_filename}'
        file_path = os.path.join(product_dir, filename)
        file.save(file_path)

        product_store.add_image(product, url=file_path)

        return {'message': 'Image was successfully uploaded.'}, status.HTTP_201_CREATED


@ns.route('/<product_id>/images/<image_id>')
class ProductImageItem(Resource):
    @jwt_required
    @active_user
    @admin_or_worker
    def delete(self, product_id, image_id):
        if not product_store.has_image(product_id, image_id):
            return {'message': 'Image not found.'}, status.HTTP_404_NOT_FOUND

        product_store.delete_image(image_id)

        return {'message': 'Image was successfully deleted.'}
