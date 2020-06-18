from sqlalchemy import CheckConstraint

from db import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"
    #__table_args__ = (
    #    CheckConstraint('pending' == 1 or 'pending' == 0 or 'pending' is None or 'pending' == True or 'pending' == False, name='check_pending_bool'),
    #    {})

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(64))
    account_id = db.Column(db.String(64))
    category_id = db.Column(db.String(64))
    transaction_type = db.Column(db.String(32))
    name = db.Column(db.String(64))
    amount = db.Column(db.Float)
    iso_currency_code = db.Column(db.String(32))
    unofficial_currency_code = db.Column(db.String(32))
    date = db.Column(db.String(10))
    authorized_date = db.Column(db.String(10))
    payment_channel = db.Column(db.String(32))
    pending = db.Column(db.Boolean, default=False)
    pending_transaction_id = db.Column(db.String(64))
    transaction_code = db.Column(db.String(64))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    item = db.relationship("ItemModel")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()