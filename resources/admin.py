import traceback

from flask import request, make_response, render_template
from flask_restful import Resource
from flask_jwt_extended import (
    fresh_jwt_required,
    jwt_required, get_raw_jwt,
)

from admin import admin_required
from models.restaurant import RestaurantModel, TagModel
from schemas.tag import TagSchema

NOT_FOUND = "Restaurant not found."
TAG_EXISTS = "Tag already exists."
TAG_CREATED_SUCCESSFULLY = "Tag created successfully."
TAG_CREATION_FAILED = "Failed to create tag."

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
            return {"message": NOT_FOUND}, 404

        headers = {"Content-Type": "text/html"}
        return make_response(render_template("admin-restaurant.html", restaurant=restaurant), 200, headers)


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

