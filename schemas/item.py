from ma import ma
from marshmallow import pre_load
from models.item import ItemModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel

        include_fk = True
        load_instance = True

    #@pre_load
    #def _pre_load(self, data, **kwargs):
    #    self.institution_id = data['institution']['institution_id']
    #    self.institution_name = data['institution']['name']
    #    return data
