from db import db
from models.transaction import TransactionModel

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.String(64), nullable=False)
    link_session_id = db.Column(db.String(64), nullable=False)
    institution_id = db.Column(db.String(64))
    institution_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel")
    transactions = db.relationship("TransactionModel", lazy="dynamic", cascade="all, delete-orphan")

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
