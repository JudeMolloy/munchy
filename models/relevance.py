from db import db


class RelevanceModel(db.Model):
    __tablename__ = "relevances"

    id = db.Column(db.Integer, primary_key=True)
    preference_rating = db.Column(db.Float, nullable=False, default=0.5, index=True)

    # Link to DeviceModel.
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    device = db.relationship("DeviceModel")

    # Link to RestaurantModel.
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False)
    restaurant = db.relationship("RestaurantModel")

