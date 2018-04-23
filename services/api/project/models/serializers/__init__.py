from enum import IntEnum

from flask_restplus import fields

from project import api


class IntEnumField(fields.Raw):
    def format(self, value: IntEnum):
        return value.name.lower().replace('_', ' ')


user = api.model('User', {
    'id': fields.Integer(),
    'email': fields.String(required=True),
    'role': fields.Integer(required=True),
    'role_name': IntEnumField(attribute='role'),
    'first_name': fields.String(),
    'last_name': fields.String(),
    'phone': fields.String(),
    'street': fields.String(),
    'zip_code': fields.String(),
    'city': fields.String(),
    'country': fields.Integer(),
    'date_of_birth': fields.Date()
})

category = api.model('Category', {
    'id': fields.Integer(),
    'name': fields.String(required=True)
})

product_image = api.model('Product image', {
    'id': fields.Integer(),
    'url': fields.String(required=True)
})

product = api.model('Product', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'count': fields.Integer(),
    'description': fields.String(),
    'price': fields.Float(required=True),
    'category': fields.Nested(category),
    'images': fields.List(fields.Nested(product_image))
})

product_rating = api.model('Product rating', {
    'id': fields.Integer(),
    'user': fields.Nested(user),
    'product': fields.Nested(product),
    'rating': fields.Integer()
})

delivery_address = api.model('DeliveryAddress', {
    'id': fields.Integer(),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'phone': fields.String(required=True),
    'street': fields.String(required=True),
    'zip_code': fields.String(required=True),
    'city': fields.String(required=True),
    'country': fields.String(required=True)
})

order_item = api.model('OrderItem', {
    'id': fields.Integer(),
    'count': fields.Integer(required=True),
    'price': fields.Float(required=True),
    'product': fields.Nested(product)
})

order = api.model('Order', {
    'id': fields.Integer(),
    'status': fields.Integer(required=True),
    'status_name': IntEnumField(attribute='status'),
    'total': fields.Float(required=True),
    'created': fields.DateTime(required=True),
    'updated': fields.DateTime(required=True),
    'items': fields.List(fields.Nested(order_item)),
    'delivery_address': fields.Nested(delivery_address),
    'user': fields.Nested(user)
})
