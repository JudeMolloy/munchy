import collections
import traceback

from flask import request, make_response, render_template
from flask_restful import Resource
from flask_jwt_extended import (
    fresh_jwt_required,
    jwt_required, get_raw_jwt,
)

from admin import admin_required
from models.restaurant import RestaurantModel, TagModel, ClipModel
from schemas.tag import TagSchema
from forms.upload_clip import UploadClipForm
from libs.upload import upload_to_vod_bucket


RESTAURANT_NOT_FOUND = "Restaurant not found."
TAG_EXISTS = "Tag already exists."
TAG_CREATED_SUCCESSFULLY = "Tag created successfully."
TAG_CREATION_FAILED = "Failed to create tag."
CLIP_UPLOADED_SUCCESSFULLY = "Clip uploaded successfully."
CLIP_UPLOAD_FAILED = "Failed to upload clip."

tag_schema = TagSchema()


class AdminHome(Resource):
    @fresh_jwt_required
    @admin_required
    @classmethod
    def get(cls):
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("admin.html"), 200, headers)


class AdminRestaurant(Resource):
    @admin_required
    @fresh_jwt_required
    @classmethod
    def get(cls, restaurant_id: str):
        # Get restaurant with ID.
        restaurant = RestaurantModel.find_by_id(restaurant_id)

        if not restaurant:
            return {"message": RESTAURANT_NOT_FOUND}, 404

        headers = {"Content-Type": "text/html"}
        return make_response(render_template("admin-restaurant.html", restaurant=restaurant), 200, headers)


class AddRestaurant(Resource):
    @classmethod
    def post(cls):
        form = AddRestaurantForm()
        return make_response(render_template("file-upload.html", form=form))


class AddTag(Resource):
    @classmethod
    def post(cls):
        tag_json = request.get_json()
        tag = tag_schema.load(tag_json)

        if TagModel.find_by_name(tag.name):
            return {"message": TAG_EXISTS}, 400

        try:
            tag.save_to_db()
            return {"message": TAG_CREATED_SUCCESSFULLY}, 201
        except:
            traceback.print_exc()
            tag.delete_from_db()
            return {"message": TAG_CREATION_FAILED}, 500


class UploadClip(Resource):
    @classmethod
    def get(cls):
        form = UploadClipForm()
        return make_response(render_template("file-upload.html", form=form))

    @classmethod
    def post(cls):
        form_data = request.form.to_dict(flat=False)  # Converts data into dict of lists to avoid duplicate keys.
        restaurants = form_data['restaurants']

        title = request.form['title']
        description = request.form['description']
        video = request.files["file"]

        if video:
            video_url = upload_to_vod_bucket(video)

            # Add the data to the database.
            clip = ClipModel(title=title, description=description, video_url=video_url)

            for restaurant_id in restaurants:
                try:
                    restaurant = RestaurantModel.find_by_id(restaurant_id)
                    # Possibly need to check that the clip doesn't already have the restaurant.
                    if not restaurant:
                        return {"message": RESTAURANT_NOT_FOUND}, 404
                    clip.restaurants.append(restaurant)
                except:
                    return {"message": CLIP_UPLOAD_FAILED}, 500

            try:
                clip.save_to_db()
                return make_response(render_template("upload-success.html", response="successful"))
            except:
                traceback.print_exc()
                clip.delete_from_db()

        return make_response(render_template("upload-success.html", response="unsuccessful"))

