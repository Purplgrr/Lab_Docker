from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.articles import Article


class ArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        exclude = ('author_id',)

    title = fields.String(
        required=True,
        validate=validate.Length(min=5)
    )

    content = fields.String(
        required=True,
        validate=validate.Length(min=5)
    )


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
