from marshmallow_sqlalchemy import ModelSchema

from project.api.models import User
from project import session


class BaseSchema(ModelSchema):
    class Meta:
        sqla_session = session


class UserSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = User


user_schema = UserSchema()
