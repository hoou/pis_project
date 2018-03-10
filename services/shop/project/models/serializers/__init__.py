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
