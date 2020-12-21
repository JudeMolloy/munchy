from ma import ma
from marshmallow import pre_dump, fields, EXCLUDE
from models.restaurant import RestaurantModel
from schemas.tag import TagSchema
from schemas.clip import ClipSchema


class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RestaurantModel
        #load_only = ("name", "bio")
        dump_only = ("id", "tags", "clips", "relevance")
        load_instance = True

        # Excludes unknown files which is an
        # error that is raised because tags is
        # passed in on input even though it is dump only.
        unknown = EXCLUDE

    tags = fields.Nested(TagSchema, many=True)
    clips = fields.Nested(ClipSchema, many=True)

