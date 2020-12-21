from db import db

class LocationModel(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    # Link to DeviceModel.
    device_id = db.Column(db.Integer, db.ForeignKey("devices.id"), nullable=False)
    device = db.relationship("DeviceModel")