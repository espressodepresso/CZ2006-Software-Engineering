from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import Form,StringField,validators
from wtforms.validators import InputRequired


class searchForm(Form):
    foodname = StringField('Search Food',validators=[InputRequired()])
