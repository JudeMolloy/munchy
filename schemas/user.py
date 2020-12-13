from ma import ma
from marshmallow import pre_dump, fields
from models.user import UserModel
from schemas.confirmation import ConfirmationSchema


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id", "confirmation")
        load_instance = True

    most_recent_confirmation = fields.Nested(ConfirmationSchema)

    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs):
        self.most_recent_confirmation = user.most_recent_confirmation
        return user



