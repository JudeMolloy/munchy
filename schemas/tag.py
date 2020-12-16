from ma import ma
from models.restaurant import TagModel


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TagModel
        #load_only = ("name",)
        dump_only = ("id",)
        include_fk = True  # So the FK is included in the dump.
        load_instance = True

