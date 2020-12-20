import traceback

from flask import request
from flask_restful import Resource
from models.restaurant import ClipModel
from schemas.clip import ClipSchema

CLIP_EXISTS = "Clip already exists."
CLIP_CREATED_SUCCESSFULLY = "Clip created successfully."
CLIP_CREATION_FAILED = "Failed to create clip."

clip_schema = ClipSchema()


class Clip(Resource):
    @classmethod
    def post(cls):
        clip_json = request.get_json()
        clip = clip_schema.load(clip_json)

        if ClipModel.find_by_name(clip.name):
            return {"message": CLIP_EXISTS}, 400

        try:
            clip.save_to_db()
            return {"message": CLIP_CREATED_SUCCESSFULLY}, 201
        except:
            traceback.print_exc()
            clip.delete_from_db()
            return {"message": CLIP_CREATION_FAILED}, 500

