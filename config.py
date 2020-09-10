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

    PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
    PLAID_SECRET = os.getenv('PLAID_SECRET')
    PLAID_PUBLIC_KEY = os.getenv('PLAID_PUBLIC_KEY')
    # Use 'sandbox' to test with Plaid's Sandbox environment (username: user_good,
    # password: pass_good)
    # Use development to test with live users and credentials and production
    # to go live
    PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'  # Production URI


class DevelopmentConfig(Config):
    DEBUG = True
    # Gmail API worsk without SSL.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class TestingConfig(Config):
    TESTING = True
