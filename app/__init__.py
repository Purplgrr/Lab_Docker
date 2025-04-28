from flask import Flask, make_response, jsonify, request, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .config import Config
from .extensions import db, jwt, ma, cache


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["300 per day", "50 per hour"]
    )

    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    from .routes.auth import auth_bp
    from .routes.drafts import drafts_bp
    from .routes.articles import articles_bp
    from .routes.aggregate import aggregate_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(drafts_bp, url_prefix='/api/drafts')
    app.register_blueprint(articles_bp, url_prefix='/api/articles')
    app.register_blueprint(aggregate_bp, url_prefix='/api/stats')

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'success': False, 'error': 'Not found'}), 404)

    @app.errorhandler(400)
    def bad_request(error):
        return make_response(jsonify({'success': False, 'error': 'Bad request'}), 400)

    with app.app_context():
        from app.schemas.user import user_schema
        from app.models import articles, drafts

        db.create_all(bind_key=['articles', 'drafts'])

    return app
