from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.articles import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # load_instance = True
        exclude = ("password_hash",)

    email = fields.Email(required=False)

    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=6)
    )

    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=80)
    )


user_schema = UserSchema()
