from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from db import db
from libs.relevance import update_relevance
from models import RelevanceModel

UPDATED_RELEVANCE_SUCCESSFUL = "Relevance ratings have been updated successfully."
UPDATED_RELEVANCE_FAILED = "Failed to update relevance ratings."

PROFILE_DATA_CREATED_SUCCESSFULLY = "Profile data has been created successfully."
PROFILE_DATA_UPDATED_SUCCESSFULLY = "Profile data has been updated successfully."
PROFILE_DATA_UPDATE_FAILED = "Failed to update profile data."


def updateData(relevance_rating, relevance_json):
    relevance_rating.profile_views += 1
    if relevance_json["favourite"] == "True":
        relevance_rating.favourite = True


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

        return {"message": UPDATED_RELEVANCE_FAILED}, 500


class UpdateProfileData(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        relevance_json = request.get_json()
        current_user_id = get_jwt_identity()
        restaurant_id = relevance_json["restaurant_id"]

        if current_user_id is not None:
            relevance_rating = RelevanceModel.query.filter_by(user_id=current_user_id, restaurant_id=restaurant_id).first()

            if relevance_rating is None:
                relevance_rating = RelevanceModel(user_id=current_user_id, restaurant_id=restaurant_id)
                updateData(relevance_rating, relevance_json)
                relevance_rating.save_to_db()
                return {"message": PROFILE_DATA_CREATED_SUCCESSFULLY}, 201


            updateData(relevance_rating, relevance_json)
            db.commit()
            return {"message": PROFILE_DATA_UPDATED_SUCCESSFULLY}, 200

        return {"message": PROFILE_DATA_UPDATE_FAILED}, 500




