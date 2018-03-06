from marshmallow_sqlalchemy import ModelSchema
from project import session
from project.models.product import Product
from project.models.user import User


class BaseSchema(ModelSchema):
    class Meta:
        sqla_session = session


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User


class ProductSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Product


user_schema = UserSchema()
product_schema = ProductSchema()
