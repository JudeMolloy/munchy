from db import db


class DeviceModel(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, index=True)
    relevance = db.relationship('RelevanceModel', backref='devices', lazy="dynamic", cascade="all, delete-orphan")
    location = db.relationship('LocationModel', backref='devices', lazy="dynamic", cascade="all, delete-orphan")

    # Link to UserModel.
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")
