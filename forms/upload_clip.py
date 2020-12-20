from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired
from models.restaurant import RestaurantModel

def selectable_restaurants():
    return RestaurantModel.query.all()

class UploadClipForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    restaurants = QuerySelectMultipleField(query_factory=selectable_restaurants)
    submit = SubmitField("Upload")