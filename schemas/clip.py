from ma import ma
from models.restaurant import ClipModel


class ClipSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ClipModel
        #load_only = ("name",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True

