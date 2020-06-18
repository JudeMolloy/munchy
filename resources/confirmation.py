import traceback
from time import time
from flask import make_response, render_template
from flask_restful import Resource

from libs.mailgun import MailgunException
from models.confirmation import ConfirmationModel
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema

confirmation_schema = ConfirmationSchema()

NOT_FOUND = "Confirmation link is invalid."
EXPIRED = "Confirmation link has expired."
ALREADY_CONFIRMED = "Account has already been confirmed."
USER_NOT_FOUND = "User does not exist."
RESEND_SUCCESSFUL = "Confirmation email successfully resent."
RESEND_FAILED = "Confirmation email failed to resend."


class Confirmation(Resource):
    @classmethod
    def get(cls, confirmation_id: str):
        # Returns the confirmation HTML page.
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        if not confirmation:
            return {"message": NOT_FOUND}, 404

        if confirmation.expired:
            print(confirmation.expired)
            print(time())
            print(confirmation.expire_at)
            return {"message": EXPIRED}, 400

        if confirmation.confirmed:
            return {"message": ALREADY_CONFIRMED}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(render_template("confirmation.html", email=confirmation.user.email), 200, headers)


class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        # Returns all the confirmations for a given user. Testing ONLY.
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return (
            {
                "current_time": int(time()),
                "confirmations": [
                    confirmation_schema.dump(each)
                    for each in user.confirmations.order_by(ConfirmationModel.expire_at).all()
                ]
            },
            200
        )

    @classmethod
    def post(cls, user_id: int):
        # Resend confirmation email.
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        try:
            confirmation = user.most_recent_confirmation
            if confirmation:
                if confirmation.confirmed:
                    return {"message": ALREADY_CONFIRMED}, 400
                confirmation.force_to_expire()

            new_confirmation = ConfirmationModel(user_id)
            new_confirmation.save_to_db()
            user.send_confirmation_email()
            return {"message": RESEND_SUCCESSFUL}, 201
        except MailgunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": RESEND_FAILED}, 500

