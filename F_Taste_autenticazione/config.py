from datetime import timedelta
from F_Taste_autenticazione.utils.credentials import secret_key
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False

class DevelopmentConfig(Config):
    RAISE_EXCEPTIONS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secret_key
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    ERROR_INCLUDE_MESSAGE  = True
    RESTX_VALIDATE = True
    RATELIMIT_ENABLED = False
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)

config = {
    'dev': DevelopmentConfig
}