from flask import request, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from libs.mailgun import Mailgun
from models.confirmation import ConfirmationModel


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # This is salted and hashed on initialisation

    # Delete orphan only works for PostgreSQL?
    confirmations = db.relationship("ConfirmationModel", lazy="dynamic", cascade="all, delete-orphan")
    relevances = db.relationship('RelevanceModel', backref='users', lazy="dynamic", cascade="all, delete-orphan", order_by="desc(RelevanceModel.rating)", primaryjoin="RelevanceModel.user_id==UserModel.id")
    locations = db.relationship('LocationModel', backref='users', lazy="dynamic", cascade="all, delete-orphan")
    clip_data = db.relationship('ClipDataModel', backref='users', lazy="dynamic", cascade="all, delete-orphan")

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    @property
    def most_recent_confirmation(self):
        return self.confirmations.order_by(db.desc(ConfirmationModel.expire_at)).first()

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for("confirmation", confirmation_id=self.most_recent_confirmation.id)
        subject = "Email Confirmation"
        text = "Click the link to confirm your account: {}".format(link)
        html = '<html><a href="{}">Click here to confirm account</a></html>'.format(link)

        return Mailgun.send_email([self.email], subject, text, html)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
