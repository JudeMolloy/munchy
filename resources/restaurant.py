import traceback

from flask import request, make_response, render_template, jsonify, url_for
from flask_restful import Resource
from models.restaurant import RestaurantModel, TagModel
from schemas.restaurant import RestaurantSchema

restaurant_schema = RestaurantSchema()

RESTAURANT_NOT_FOUND = "Restaurant not found."
RESTAURANT_CREATED_SUCCESSFULLY = "Restaurant has been created successfully."
CREATION_FAILED = "Failed to create restaurant."
RESTAURANTS_FETCH_FAILED = "Failed to fetch restaurants."

TAG_NOT_FOUND = "Tag not found."


class Restaurant(Resource):
    @classmethod
    # @jwt_required
    def get(cls, restaurant_id: int):
        restaurant = RestaurantModel.find_by_id(restaurant_id)
        if not restaurant:
            return {"message": RESTAURANT_NOT_FOUND}, 404

        return restaurant_schema.dump(restaurant), 200


class AddRestaurant(Resource):
    @classmethod
    # @jwt_required
    def post(cls):
        restaurant_json = request.get_json()
        print(restaurant_json)
        restaurant = restaurant_schema.load(restaurant_json)
        print(restaurant)

        tags = restaurant_json["tags"]
        print(restaurant_json["tags"])

        for tag_id in tags:
            try:
                tag = TagModel.find_by_id(tag_id)
                # Possibly need to check that the restaurant doesn't already have the tag.
                if not tag:
                    return {"message": TAG_NOT_FOUND}, 404
                restaurant.tags.append(tag)
            except:
                return {"message": CREATION_FAILED}, 500

        try:
            restaurant.save_to_db()
            return {"message": RESTAURANT_CREATED_SUCCESSFULLY}, 201
        except:
            traceback.print_exc()
            restaurant.delete_from_db()
            return {"message": CREATION_FAILED}, 500


class Restaurants(Resource):
    @classmethod
    def get(cls):
        restaurants = RestaurantModel.query.all()
        try:
            return (
                {
                    "restaurants": [
                        restaurant_schema.dump(restaurant)
                        for restaurant in restaurants
                    ]
                },
                200
            )
        except:
            return {"message": RESTAURANTS_FETCH_FAILED}, 500