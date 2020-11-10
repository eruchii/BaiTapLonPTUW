
from flask_wtf import FlaskForm
# from wtforms import StringField
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from easyaccomod.owner_models import City


class SearchForm(FlaskForm):
    qry = City.query.all()
    citiest =[]
    for city in qry:
        citiest.append(city.name)
    city = SelectField("Choose your City",choices=citiest)
    district = SelectField("Choose your District",choices=None)
    street = SelectField("Choose your Street",choices=None)
    submit = SubmitField("Search")
