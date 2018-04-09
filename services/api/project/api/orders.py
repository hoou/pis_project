from typing import Dict

from flask import request
from flask_api import status
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from flask_restplus import Resource

from project import api
from project.api.errors import InvalidPayload, BadRequest, NotFound
from project.api.middleware.auth import active_required_if_logged_in, admin_or_worker
from project.business import orders, products
from project.models.delivery_address import DeliveryAddress
from project.models.order import OrderStatus
from project.models.order_item import OrderItem as OrderItemModel
from project.models.serializers import order as order_serial
from project.utils.list import has_duplicates

ns = api.namespace('orders')


@ns.route('/')
class OrderCollection(Resource):
    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    @api.marshal_list_with(order_serial)
    def get(self):
        return orders.get_all()

    @jwt_optional
    @active_required_if_logged_in
    def post(self):
        data = request.get_json()

        user_id = get_jwt_identity()

        if not data:
            raise InvalidPayload

        items = data.get('items')
        delivery_address = data.get('delivery_address')

        if items is None or delivery_address is None:
            raise InvalidPayload

        if len(items) == 0:
            raise BadRequest('Order without items.')

        item_ids = [item.get('product_id') for item in items]
        if has_duplicates(item_ids):
            raise InvalidPayload

        try:
            delivery_address = DeliveryAddress(**delivery_address)
        except TypeError:
            raise InvalidPayload

        order_items = []

        for item in items:  # type: Dict
            product_id = item.get('product_id')
            count = item.get('count')
            if product_id is None or count is None:
                raise InvalidPayload

            product = products.get(item['product_id'])
            if product is None:
                raise NotFound('Product not found.')

            if not isinstance(item['count'], int) or item['count'] <= 0:
                raise BadRequest('Item count must be positive int.')

            order_items.append(OrderItemModel(item['count'], product.price, product.id))

        orders.add(order_items, delivery_address, user_id)

        return {'message': 'Order was successfully created.'}, status.HTTP_201_CREATED


@ns.route('/<int:order_id>')
class OrderItem(Resource):
    @jwt_required
    @active_required_if_logged_in
    @api.marshal_with(order_serial)
    def get(self, order_id: int):
        order = orders.get(order_id)

        if order is None:
            raise NotFound('Order not found.')

        user_id = get_jwt_identity()

        if order.user_id != user_id:
            raise BadRequest('Order is not your\'s.')

        return order

    @jwt_required
    @active_required_if_logged_in
    @admin_or_worker
    def patch(self, order_id: int):
        order = orders.get(order_id)
        if order is None:
            raise NotFound('Order not found.')

        data = request.get_json()
        if not data:
            raise InvalidPayload

        order_status = data.get('status')
        if order_status is None:
            raise InvalidPayload

        done = orders.change_status(order, order_status)

        if not done:
            raise InvalidPayload

        return {'message': 'Order was successfully modified.'}


@ns.route('/<int:order_id>/cancel')
class OrderItemCancel(Resource):
    @jwt_required
    @active_required_if_logged_in
    def patch(self, order_id: int):
        order = orders.get(order_id)
        if order is None:
            raise NotFound('Order not found.')

        if order.status == OrderStatus.CANCELLED:
            raise BadRequest('Order is already cancelled.')

        user_id = get_jwt_identity()

        if order.user_id != user_id:
            raise BadRequest('You cannot cancel other\'s order.')

        orders.cancel(order)

        return {'message': 'Order was successfully cancelled.'}
