
from flask_wtf import FlaskForm
# from wtforms import StringField
from wtforms.fields.core import BooleanField, SelectField,StringField,IntegerField
from wtforms.fields.simple import PasswordField, SubmitField
# from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from easyaccomod.owner_models import City


class SearchForm(FlaskForm):
    qry = City.query.all()
    citiest =[""]
    for city in qry:
        citiest.append(city.name)
    city = SelectField("Choose your City",choices=citiest)
    district = SelectField("Choose your District",choices=None)
    street = SelectField("Choose your Street",choices=None)
    near = StringField("Near which University")
    price = StringField("Price")
    roomType = StringField("Room Type")
    area = StringField("Area")
    chung_chu = BooleanField("Host?")
    phong_tam = IntegerField("Number of Shower Room?")
    nong_lanh = BooleanField("Binh nong lanh")
    dieu_hoa = BooleanField("Dieu hoa")
    ban_cong = BooleanField("Binh nong lanh")
    gia_dien = IntegerField("Gia dien")
    gia_nuoc = IntegerField("Gia nuoc")
    tien_ich_khac = StringField("Tien ich Khasc")
    submit = SubmitField("Search")
