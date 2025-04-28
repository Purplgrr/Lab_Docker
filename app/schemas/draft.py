from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.drafts import Draft


class DraftSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Draft
        exclude = ('author_id',)

    title = fields.String(
        required=True,
        validate=validate.Length(min=5)
    )

    content = fields.String(
        required=True,
        validate=validate.Length(min=5)
    )


draft_schema = DraftSchema()
drafts_schema = DraftSchema(many=True)
