import traceback

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
    get_raw_jwt,
    get_jti,
)
from libs.mailgun import MailgunException
from blacklist import ACCESS_EXPIRES, REFRESH_EXPIRES, revoked_store
from models.user import UserModel
from models.confirmation import ConfirmationModel
from schemas.user import UserSchema

user_schema = UserSchema()

# Messages
USER_EMAIL_EXISTS = "A user with that email already exists."
USER_REGISTERED = "User has been successfully registered."
USER_NOT_FOUND = "User not found."
USER_INVALID_CREDENTIALS = "Username or password is incorrect."
ADMIN_PRIVILEGES_REQUIRED = "Admin privileges are required for this action."
LOGOUT = "Successfully logged out."
NOT_CONFIRMED = "Account not confirmed. Please check your email: {}."
CREATION_FAILED = "Failed to create user."
USER_CREATED_SUCCESSFULLY = "Account has been created successfully. An activation link has been sent to your email."
USER_DELETE_FAILED = "Something went wrong when deleting your account."
USER_DELETE_SUCCESSFUL = "Your account has been deleted."


class User(Resource):
    @classmethod
    @jwt_required
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

        try:
            user.save_to_db()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": USER_CREATED_SUCCESSFULLY}, 201
        except MailgunException as e:
            user.delete_from_db()  # Must delete user as they won't be able to confirm account.
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {"message": CREATION_FAILED}, 500


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
            confirmation = user.most_recent_confirmation
            if confirmation and confirmation.confirmed:
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)

                # Store the tokens in redis with a status of not currently revoked. We
                # can use the `get_jti()` method to get the unique identifier string for
                # each token. We can also set an expires time on these tokens in redis,
                # so they will get automatically removed after they expire. We will set
                # everything to be automatically removed shortly after the token expires
                access_jti = get_jti(encoded_token=access_token)
                refresh_jti = get_jti(encoded_token=refresh_token)
                print("ACCESS JTI = {}".format(access_jti))
                print("REFRESH JTI = {}".format(refresh_jti))
                revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
                revoked_store.set(refresh_jti, 'false', REFRESH_EXPIRES * 1.2)

                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            return {"message": NOT_CONFIRMED.format(user.email)}, 400

        return {"message": USER_INVALID_CREDENTIALS}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()['jti']  # jti is a unique identifier for a jwt.
        revoked_store.set(jti, 'true', REFRESH_EXPIRES * 1.2)
        return {"message": LOGOUT}, 200


class UserDelete(Resource):
    # Fresh JWT required as this is a powerful action
    @classmethod
    @fresh_jwt_required
    def delete(cls):
        # Find the current user. Users can only delete their own account.
        current_user_id = get_jwt_identity()
        current_user = UserModel.find_by_id(current_user_id)

        if current_user:
            try:
                current_user.delete_from_db()
                return {"message": USER_DELETE_SUCCESSFUL}, 200
            except:
                return {"message": USER_DELETE_FAILED}, 500


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        access_jti = get_jti(encoded_token=new_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)
        return {"access_token": new_token}, 200
