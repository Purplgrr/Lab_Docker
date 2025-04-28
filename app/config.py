import os
from datetime import timedelta

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    SQLALCHEMY_BINDS = {
        'drafts': os.getenv('DRAFTS_URL'),
        'articles': os.getenv('ARTICLES_URL'),
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    JWT_TOKEN_LOCATION = ['headers']

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.getenv('REDIS_URL')
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('REDIS_CACHE_TTL', 300))
    CACHE_KEY_PREFIX = 'flask_cache_'
    CACHE_SERIALIZER = 'json'
