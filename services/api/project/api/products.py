import ntpath
import os
import pathlib
import time

from flask import request, current_app
from flask_api import status
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource

from project.api import api
from project.api.errors import InvalidPayload, NotFound, BadRequest, ProductRatingError
from project.api.middleware.auth import active_required_if_logged_in, admin_or_worker
from project.business import products, users
from project.utils.file import is_uploaded_file_allowed
from project.models.serializers import product as product_serial
from project.models.serializers import product_image as product_image_serial
from project.models.serializers import product_rating as product_rating_serial

ns = api.namespace('products')


@ns.route('/')
class ProductCollection(Resource):
    @api.marshal_list_with(product_serial)
    def get(self):
        return products.get_all()


@ns.route('/deleted')
class DeletedProductCollection(Resource):
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    @api.marshal_list_with(product_serial)
    def get(self):
        return products.get_all_deleted()


@ns.route('/<int:product_id>')
class ProductItem(Resource):
    @api.marshal_with(product_serial)
    def get(self, product_id):
        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        return product

    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def delete(self, product_id):
        product = products.get(product_id)
        if not product:
            raise NotFound('Product not found.')

        products.delete(product)

        return {'message': 'Product was successfully deleted.'}

    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def patch(self, product_id):
        data = request.get_json()

        current_app.logger.info(data)

        if not data:
            raise InvalidPayload

        product = products.get(product_id)
        if not product:
            raise NotFound('Product not found.')

        attributes = {'name', 'price', 'description', 'category_id'}

        if not any(data.get(attribute) for attribute in attributes):
            raise InvalidPayload

        try:
            products.update(product, attributes, data)
        except (TypeError, ValueError) as e:
            raise BadRequest(str(e))

        return {'message': 'Product was successfully modified.'}


@ns.route('/<int:product_id>/images')
class ProductImageCollection(Resource):
    @api.marshal_list_with(product_image_serial)
    def get(self, product_id):
        return products.get_images(product_id)

    @jwt_required
    @active_required_if_logged_in
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
    @active_required_if_logged_in
    @admin_or_worker
    def delete(self, product_id, image_id):
        if not products.has_image(product_id, image_id):
            raise NotFound('Image not found.')

        products.delete_image(image_id)

        return {'message': 'Image was successfully deleted.'}


@ns.route('/<int:product_id>/ratings')
class ProductRatingCollection(Resource):
    @api.marshal_list_with(product_rating_serial)
    def get(self, product_id):
        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        return products.get_ratings(product)

    @jwt_required
    @active_required_if_logged_in
    def post(self, product_id):
        data = request.get_json()

        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        user_id = get_jwt_identity()
        user = users.get(user_id)

        if products.get_product_rating_by_user(product, user) is not None:
            raise BadRequest('This user already rated this product.')

        rating = data.get('rating')

        if rating is None:
            raise InvalidPayload

        if not isinstance(rating, int):
            raise ProductRatingError

        if not (1 <= rating <= 5):
            raise ProductRatingError

        products.add_rating(product, user, rating)

        return {'message': 'Rating was successfully added.'}, status.HTTP_201_CREATED

    @jwt_required
    @active_required_if_logged_in
    def delete(self, product_id):
        product = products.get(product_id)

        if product is None:
            raise NotFound('Product not found.')

        user_id = get_jwt_identity()
        user = users.get(user_id)

        rating = products.get_product_rating_by_user(product, user)

        if rating is None:
            raise NotFound('Rating not found.')

        products.delete_rating(product, user)

        return {'message': 'Rating was successfully deleted.'}, status.HTTP_200_OK
