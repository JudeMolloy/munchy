from flask import request, make_response, render_template
from flask_restful import Resource
from flask_jwt_extended import (
    fresh_jwt_required,
    jwt_required, get_raw_jwt,
)

from admin import admin_required

from models.restaurant import RestaurantModel, TagModel

NOT_FOUND = "Restaurant not found."


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