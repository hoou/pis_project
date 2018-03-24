import ntpath
import os
import pathlib
import time

from flask import request, current_app
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from project.api import api
from project.api.errors import InvalidPayload, NotFound, BadRequest
from project.api.middleware.auth import active_user, admin_or_worker
from project.business import products
from project.utils.file import is_uploaded_file_allowed
from project.models.serializers import product as product_serial
from project.models.serializers import product_image as product_image_serial

ns = api.namespace('products')


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(product_serial)
    def get(self):
        return products.get_all()


@ns.route('/<int:product_id>')
class ProductItem(Resource):
    @api.marshal_with(product_serial)
    def get(self, product_id):
        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        return product

    @jwt_required
    @active_user
    @admin_or_worker
    def delete(self, product_id):
        product = products.get(product_id)
        if not product:
            raise NotFound('Product not found.')

        products.delete(product)

        return {'message': 'Product was successfully deleted.'}


@ns.route('/<int:product_id>/images')
class ProductImageCollection(Resource):
    @api.marshal_list_with(product_image_serial)
    def get(self, product_id):
        return products.get_images(product_id)

    @jwt_required
    @active_user
    @admin_or_worker
    def post(self, product_id):
        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        file = request.files.get('file')

        if file is None:
            raise InvalidPayload

        if not is_uploaded_file_allowed(file.filename):
            raise BadRequest('File extension not allowed.')

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

        products.add_image(product, url=file_path)

        return {'message': 'Image was successfully uploaded.'}, status.HTTP_201_CREATED


@ns.route('/<int:product_id>/images/<int:image_id>')
class ProductImageItem(Resource):
    @jwt_required
    @active_user
    @admin_or_worker
    def delete(self, product_id, image_id):
        if not products.has_image(product_id, image_id):
            raise NotFound('Image not found.')

        products.delete_image(image_id)

        return {'message': 'Image was successfully deleted.'}
