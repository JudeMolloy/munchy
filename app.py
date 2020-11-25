import os
import json
from functools import wraps

from flask import Flask, jsonify, render_template, request
from flask_restful import Api
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from marshmallow import ValidationError
from werkzeug.utils import redirect

from blacklist import revoked_store

from db import db
from ma import ma
from resources.user import (
    UserRegister,
    User,
    UserLogin,
    TokenRefresh,
    UserLogout,
    UserDelete,
    AdminLogin,
)
from resources.confirmation import Confirmation, ConfirmationByUser
from resources.admin import AdminHome, AdminRestaurant

app = Flask(__name__)

api = Api(app)

jwt = JWTManager(app)

# List of user_id's for admin users.
ADMIN_IDENTITIES = [1,]

EXPIRED_TOKEN = "The token has expired."
INVALID_TOKEN = "The token is invalid."
UNAUTHORIZED = "An access token is required."
NEEDS_FRESH_TOKEN = "A fresh token is required."
REVOKED_TOKEN = "The token has been revoked."


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity in ADMIN_IDENTITIES:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token["jti"]
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == "true"


# Called when an expired token is used.
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description": EXPIRED_TOKEN,
        "error": "token_expired"
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": INVALID_TOKEN,
        "error": "invalid_token"
    }), 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return jsonify({
        "description": UNAUTHORIZED,
        "error": "authorization_required"
    }), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback():
    return jsonify({
        "description": NEEDS_FRESH_TOKEN,
        "error": "fresh_token_required"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": REVOKED_TOKEN,
        "error": "revoked_token"
    }), 401


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserDelete, "/user-delete")
api.add_resource(TokenRefresh, "/token-refresh")
api.add_resource(Confirmation, "/user-confirmation/<string:confirmation_id>")

api.add_resource(AdminLogin, "/admin/login")

# Possibly just change to resend confirmation. Get rid of get method for testing.
api.add_resource(ConfirmationByUser, "/confirmation/user/<int:user_id>")


# Admin


# Registers the db and marshmallow with the app .
if __name__ == "__main__":
    app.config.from_object("config.DevelopmentConfig")  # Can change this to production or testing.
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)















