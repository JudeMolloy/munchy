from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from db import db
from models.data import ClipDataModel


CLIP_DATA_CREATED_SUCCESSFULLY = "Clip data has been created successfully."
CLIP_DATA_UPDATED_SUCCESSFULLY = "Clip data has been updated successfully."
CLIP_DATA_UPDATE_FAILED = "Failed to update clip data."


def updateData(clip, clip_data_json):
    if clip_data_json["liked"] == "True":
        clip.increment_likes()

    clip.views += clip_data_json["views"]
    clip.share_clicks += clip_data_json["share_clicks"]
    clip.map_clicks += clip_data_json["map_clicks"]
    clip.deliveroo_clicks += clip_data_json["deliveroo_clicks"]
    clip.uber_eats_clicks += clip_data_json["uber_eats_clicks"]
    clip.just_eat_clicks += clip_data_json["just_eat_clicks"]

class ClipData(Resource):
    @jwt_required
    def post(self):
        clip_data_json = request.get_json()

        clip_id = clip_data_json["clip_id"]

        current_user_id = get_jwt_identity()

        if current_user_id is not None:
            clip = ClipDataModel.query.filter_by(user_id=current_user_id, clip=clip_id).first()

            if clip is None:
                clip = ClipDataModel(user_id=current_user_id, clip=clip_id)
                updateData(clip, clip_data_json)
                clip.save_to_db()
                return {"message": CLIP_DATA_CREATED_SUCCESSFULLY}, 201

            updateData(clip, clip_data_json)
            db.session.commit()

            return {"message": CLIP_DATA_UPDATED_SUCCESSFULLY}, 200

        return {"message": CLIP_DATA_UPDATE_FAILED}, 500



