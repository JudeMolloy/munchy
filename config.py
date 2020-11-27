import os

from blacklist import ACCESS_EXPIRES, REFRESH_EXPIRES

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-difficult-to-guess-key'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True

    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_BLACKLIST_ENABLED= True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # Cookie config
    JWT_COOKIE_SECURE = False
    JWT_ACCESS_TOKEN_PATH = '/admin'
    JWT_REFRESH_COOKIE_PATH = '/admin/token/refresh'
    JWT_COOKIE_CSRF_PROTECT = True

    # Allows JWT cookies to work with HTML forms.
    JWT_CSRF_CHECK_FORM = True

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'very-difficult-to-guess-key'




class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'  # Production URI


class DevelopmentConfig(Config):
    DEBUG = True
    # Gmail API worsk without SSL.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class TestingConfig(Config):
    TESTING = True
