from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app.models.drafts import Draft
from app.models.articles import Article
from app import db
from app.schemas.draft import draft_schema, drafts_schema
from app.schemas.article import article_schema


drafts_bp = Blueprint('drafts', __name__)


@drafts_bp.route('/', methods=['GET'])
@jwt_required()
def get_drafts():
    drafts = Draft.query.filter(Draft.author_id == get_jwt_identity()).all()
    return jsonify({'success': True, 'drafts': drafts_schema.dump(drafts)}), 200


@drafts_bp.route('/<int:draft_id>', methods=['GET'])
@jwt_required()
def get_draft(draft_id):
    author_id = get_jwt_identity()

    draft = Draft.query.filter(
        Draft.id == draft_id,
        Draft.author_id == author_id
    ).one_or_none()

    if draft is None:
        return jsonify({
            "success": False,
            "error": "Draft not found or you do not have permission to access it."
        }), 404

    return jsonify({
        "success": True,
        "draft": draft_schema.dump(draft)
    }), 200


@drafts_bp.route('/<int:draft_id>', methods=['PATCH'])
@jwt_required()
def update_draft(draft_id):
    author_id = get_jwt_identity()

    draft = Draft.query.filter(
        Draft.id == draft_id,
        Draft.author_id == author_id
    ).one_or_none()

    if draft is None:
        return jsonify({
            "success": False,
            "error": "Draft not found or you do not have permission to access it."
        }), 404

    request_json = request.get_json()

    if 'title' in request_json:
        draft.title = request_json['title']
    if 'content' in request_json:
        draft.content = request_json['content']

    db.session.commit()

    return jsonify({
        "success": True,
        "draft": draft_schema.dump(draft)
    }), 200


@drafts_bp.route('/<int:draft_id>', methods=['DELETE'])
@jwt_required()
def delete_draft(draft_id):
    author_id = get_jwt_identity()

    draft = Draft.query.filter(
        Draft.id == draft_id,
        Draft.author_id == author_id
    ).one_or_none()

    if draft is None:
        return jsonify({
            "success": False,
            "error": "Draft not found or you do not have permission to delete it."
        }), 404

    db.session.delete(draft)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Draft successfully deleted."
    }), 204


@drafts_bp.route('/', methods=['POST'])
@jwt_required()
def create_draft():
    try:
        request_json = request.get_json()
        validated_data = draft_schema.load(request_json, session=db.session)

        draft = Draft(
            title=validated_data['title'],
            content=validated_data['content'],
            author_id=get_jwt_identity(),
        )

        db.session.add(draft)
        db.session.commit()

        return jsonify({
            "draft": draft_schema.dump(draft),
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


@drafts_bp.route('/publish/<int:draft_id>', methods=['POST'])
@jwt_required()
def publish_draft(draft_id):
    try:
        author_id = get_jwt_identity()

        draft = Draft.query.filter(
            Draft.id == draft_id,
            Draft.author_id == author_id
        ).one_or_none()

        if draft is None:
            return jsonify({
                "success": False,
                "error": "Draft not found or you do not have permission to delete it."
            }), 404

        article = Article(
            title=draft.title,
            content=draft.content,
            author_id=get_jwt_identity(),
            published_at=db.func.now()
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
