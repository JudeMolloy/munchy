from ma import ma
from models.data import ClipDataModel

# Not sure I need this but I'll keep for the time being.
class ClipDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClipDataModel
        # load_only = ("name", "bio")
        dump_only = ("id")
        load_instance = True
