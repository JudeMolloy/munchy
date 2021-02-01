from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from libs.relevance import update_relevance


UPDATED_RELEVANCE_SUCCESSFUL = "Relevance ratings have been updated successfully."
UPDATED_RELEVANCE_FAILED = "Failed to update relevance ratings."



class UpdateRelevance(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        # Find the current user. Users can only update their own relevance values.
        current_user_id = get_jwt_identity()

        if current_user_id is not None:
            # Probably need this https://docs.sqlalchemy.org/en/14/dialects/mysql.html?highlight=upsert#insert-on-duplicate-key-update-upsert
            # NEED TO UPSERT RELEVANCE!!!
            update_relevance(current_user_id)
            return {"message": UPDATED_RELEVANCE_SUCCESSFUL}, 200

        return {"message": UPDATED_RELEVANCE_SUCCESSFUL}, 500

