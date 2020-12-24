
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from easyaccomod.owner_models import City


class SearchForm(FlaskForm):
    qry = City.query.all()
    cities =[]
    for city in qry:
        cities.append(city.name)

    city = SelectField("Choose your City",choices=cities,_name="city")
    district = SelectField("Choose your District",choices=None,_name="district")
    street = SelectField("Choose your Street",choices=None,_name="street")
    submit = SubmitField("Go!",_name=None)
