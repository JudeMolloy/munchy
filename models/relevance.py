from db import db


class RelevanceModel(db.Model):
    __tablename__ = "relevances"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False, index=True)

    # Data
    favourite = db.Column(db.Boolean, default=False)
    profile_views = db.Column(db.Integer, default=0)

    # Link to UserModel.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")

    # Link to RestaurantModel.
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    restaurant = db.relationship("RestaurantModel")

    def __init__(self, user_id, restaurant_id, rating=0.5):
        self.rating = rating
        self.user_id = user_id
        self.restaurant_id = restaurant_id

    def increment_profile_views(self):
        self.profile_views += 1

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()