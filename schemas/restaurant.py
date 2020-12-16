from ma import ma
from marshmallow import pre_dump, fields
from models.restaurant import RestaurantModel
from schemas.tag import TagSchema


class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RestaurantModel
        #load_only = ("name", "bio")
        dump_only = ("id", "tags")
        load_instance = True

    tags = fields.Nested(TagSchema)

    @pre_dump
    def _pre_dump(self, restaurant: RestaurantModel, **kwargs):
        self.tags = restaurant.get_tags
        return restaurant

