from flask import Blueprint, jsonify

from sqlalchemy import func
from app.models.articles import Article
from app.models.drafts import Draft
from app import db, cache


aggregate_bp = Blueprint('aggregate', __name__)


@aggregate_bp.route('/users/article-count')
@cache.cached(key_prefix='user_article_count')
def get_user_article_count():
    query = (
        db.session.query(
            Article.author_id.label("author_id"),
            func.count(Article.author_id).label("article_count")
        )
        .group_by(Article.author_id)
    )

    results = query.all()

    if not results:
        return jsonify({'success': True, 'article_counts': []})

    article_counts = [
        {'author_id': row.author_id, 'article_count': row.article_count}
        for row in results
    ]

    return jsonify({'success': True, 'article_counts': article_counts})


@aggregate_bp.route('/users/draft-count')
@cache.cached(key_prefix='user_draft_count')
def get_user_draft_count():
    query = (
        db.session.query(
            Draft.author_id.label("author_id"),
            func.count(Draft.author_id).label("draft_count")
        )
        .group_by(Draft.author_id)
    )

    results = query.all()

    if not results:
        return jsonify({'success': True, 'draft_counts': []})

    draft_counts = [{'author_id': author_id, 'draft_count': article_count}
                      for author_id, article_count in results]

    return jsonify({'success': True, 'draft_counts': draft_counts})
