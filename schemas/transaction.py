from ma import ma
from models.transaction import TransactionModel
from marshmallow import EXCLUDE


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TransactionModel
        include_fk = True
        load_instance = True

        unknown = EXCLUDE #exclude unknown fields
