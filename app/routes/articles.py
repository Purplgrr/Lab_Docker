from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.articles import Article
from app import db
from app.schemas.article import article_schema, articles_schema


articles_bp = Blueprint('articles', __name__)


@articles_bp.route('/', methods=['GET'])
@jwt_required()
def get_articles():
    articles = Article.query.filter(Article.author_id == get_jwt_identity()).all()
    return jsonify({'success': True, 'articles': articles_schema.dump(articles)}), 200


@articles_bp.route('/<int:article_id>', methods=['GET'])
@jwt_required()
def get_article(article_id):
    author_id = get_jwt_identity()

    article = Article.query.filter(
        Article.id == article_id,
        Article.author_id == author_id
    ).one_or_none()

    if article is None:
        return jsonify({
            "success": False,
            "error": "Article not found or you do not have permission to access it."
        }), 404

    return jsonify({
        "success": True,
        "article": article_schema.dump(article)
    }), 200


@articles_bp.route('/<int:article_id>', methods=['PATCH'])
@jwt_required()
def update_article(article_id):
    author_id = get_jwt_identity()

    article = Article.query.filter(
        Article.id == article_id,
        Article.author_id == author_id
    ).one_or_none()

    if article is None:
        return jsonify({
            "success": False,
            "error": "Article not found or you do not have permission to access it."
        }), 404

    request_json = request.get_json()

    if 'title' in request_json:
        article.title = request_json['title']
    if 'content' in request_json:
        article.content = request_json['content']

    db.session.commit()

    return jsonify({
        "success": True,
        "article": article_schema.dump(article)
    }), 200


@articles_bp.route('/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    author_id = get_jwt_identity()

    article = Article.query.filter(
        Article.id == article_id,
        Article.author_id == author_id
    ).one_or_none()

    if article is None:
        return jsonify({
            "success": False,
            "error": "Article not found or you do not have permission to delete it."
        }), 404

    db.session.delete(article)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Article successfully deleted."
    }), 204


@articles_bp.route('/', methods=['POST'])
@jwt_required()
def create_draft():
    try:
        request_json = request.get_json()
        validated_data = article_schema.load(request_json, session=db.session)

        article = Article(
            title=validated_data['title'],
            content=validated_data['content'],
            author_id=get_jwt_identity(),
        )

        db.session.add(article)
        db.session.commit()

        return jsonify({
            "article": article_schema.dump(article),
            "success": True
        }), 201

    except ValidationError as err:
        db.session.rollback()
        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
