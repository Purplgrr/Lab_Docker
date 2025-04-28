from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
import redis
from flask_caching import Cache


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
cache = Cache()
