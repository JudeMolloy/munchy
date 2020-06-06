from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt_claims,
    jwt_required,
    jwt_refresh_token_required,
    fresh_jwt_required,
)

from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()

#Messages
USER_EMAIL_EXISTS = "A user with that email already exists."
USER_REGISTERED = "User has been successfully registered."
USER_NOT_FOUND = "User not found."
USER_INVALID_CREDENTIALS = "Username or password is incorrect."
ADMIN_PRIVILEGES_REQUIRED = "Admin privileges are required for this action."


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_email(user.email):
            return {"message": USER_EMAIL_EXISTS}, 400

        user.save_to_db()

        return {"message": USER_REGISTERED}, 201

    @classmethod
    def delete(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": ADMIN_PRIVILEGES_REQUIRED}, 401



class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        '''
        Getting data straight from JSON (not using schema) 
        to get the data as the raw password is needed for comparison.
        '''
        email = user_json['email']
        password = user_json['password']

        user = UserModel.find_by_email(email)

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": USER_INVALID_CREDENTIALS}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
