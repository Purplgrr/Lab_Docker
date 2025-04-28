from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from app.models.articles import User
from app import db
from app.schemas.user import user_schema


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        request_json = request.get_json()
        validated_data = user_schema.load(request_json, session=db.session)

        if ('email' in validated_data
           and User.query.filter_by(email=validated_data['email']).first()):
            raise ValidationError({"email": ["Email already exists"]})

        if User.query.filter_by(username=validated_data['username']).first():
            raise ValidationError({"username": ["Username already exists"]})

        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', None)
        )
        user.set_password(validated_data['password'])

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "user": user_schema.dump(user),
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


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        request_json = request.get_json()
        validated_data = user_schema.load(request_json, session=db.session)

        user = (User.query.filter_by(username=validated_data['username'])
                          .one_or_404())

        if user and user.check_password(validated_data['password']):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                "success": True,
                "access_token": access_token,
            }), 200
        return jsonify({"success": False, 'error': 'Bad credentials'}), 401

    except ValidationError as err:
        return jsonify({
            "success": False,
            "errors": err.messages
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# @auth_bp.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200
