from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Optional
from models.restaurant import TagModel, ClipModel

def selectable_tags():
    return TagModel.query.all()

def selectable_clips():
    return ClipModel.query.all()

class RestaurantForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    bio = StringField("Bio")
    longitude = FloatField("Longitude", validators=[DataRequired()])
    latitude = FloatField("Latitude", validators=[DataRequired()])

    deliveroo_url = StringField("Deliveroo URL")
    ubereats_url = StringField("Uber Eats URL")
    justeat_url = StringField("Just Eat URL")

    submit = SubmitField("Submit")