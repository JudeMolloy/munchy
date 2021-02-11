import random

from models import RestaurantModel
from models.user import UserModel
from models.relevance import RelevanceModel
from db import db

from sqlalchemy.dialects.postgresql import insert


def update_relevance(current_user_id):
    '''WILL NEED TO UPDATE THIS TO FIGURE OUT RADIUS FROM CURRENT LOCATION
       IT WILL SUFFICE FOR NOW TO JUST SET FOR ALL RESTAURANTS.'''

    restaurants = RestaurantModel.query.all()  # This is what needs to change.

    for restaurant in restaurants:
        # THIS IS PROBABLY REALLY INEFFICIENT BUT IT'S THE MVP SO FORGIVE ME...
        # Check if user already has a relevance rating for the restaurant.
        relevance_rating = RelevanceModel.query.filter_by(user_id=current_user_id, restaurant=restaurant).first()

        if relevance_rating is None:
            # INSERT
            # This will set the rating to the default (0.5).
            relevance_rating = RelevanceModel(user_id=current_user_id,
                                              restaurant_id=restaurant.id)  # Can implement complex algorithm.
            relevance_rating.save_to_db()
        else:
            updated_value = random.randint(0, 100) # This can change to a function call in the future.
            relevance_rating.rating = updated_value
            db.session.commit()
