from flask import request
from flask_api import status
from flask_jwt_extended import jwt_required
from flask_restplus import Resource

from project.api.errors import InvalidPayload, NotFound, BadRequest
from project.api.middleware.auth import active_required_if_logged_in, admin_or_worker
from project.business import categories
from project.models.category import Category
from project.models.product import Product
from project.models.serializers import category as category_serial

from project import api

ns = api.namespace('categories')


@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_list_with(category_serial)
    def get(self):
        return categories.get_all()

    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def post(self):
        data = request.get_json()

        if not data:
            raise InvalidPayload

        name = data.get('name')

        if name is None:
            raise InvalidPayload

        categories.add(Category(name=name))

        return {'message': 'Category was successfully added.'}, status.HTTP_201_CREATED


@ns.route('/<int:category_id>')
class CategoryItem(Resource):
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def delete(self, category_id):
        category = categories.get(category_id)
        if not category:
            raise NotFound('Category not found.')

        if len(category.products) != 0:
            raise BadRequest('Category contains products.')

        categories.delete(category_id)

        return {'message': 'Category was successfully deleted.'}

    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def put(self, category_id):
        data = request.get_json()

        category = categories.get(category_id)
        if not category:
            raise NotFound('Category not found.')

        name = data.get('name')

        if name is None:
            raise InvalidPayload

        categories.change_name(category, name)

        return {'message': 'Category was successfully modified.'}


@ns.route('/<int:category_id>/products')
class CategoryProductCollection(Resource):
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def post(self, category_id):
        data = request.get_json()

        if not data:
            raise InvalidPayload

        name = data.get('name')
        price = data.get('price')
        count = data.get('count')
        description = data.get('description')

        if name is None or price is None:
            raise InvalidPayload

        category = categories.get(category_id)

        if category is None:
            raise NotFound('Category not found.')

        product = Product(name=name, price=price, description=description, count=count or 0)
        categories.add_product(category, product)

        return {'message': 'Product was successfully added.', 'data': {'id': product.id}}, status.HTTP_201_CREATED
