from flask_restplus import fields

from project import api

user = api.model('User', {
    'id': fields.Integer(),
    'email': fields.String(required=True)
})

product = api.model('Product', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'description': fields.String(),
    'price': fields.Float(required=True)
})

product_image = api.model('Product image', {
    'id': fields.Integer(),
    'url': fields.String(required=True)
})

product_rating = api.model('Product rating', {
    'id': fields.Integer(),
    'user': fields.Nested(user),
    'product': fields.Nested(product),
    'rating': fields.Integer()
})

category = api.model('Category', {
    'id': fields.Integer(),
    'name': fields.String(required=True)
})
