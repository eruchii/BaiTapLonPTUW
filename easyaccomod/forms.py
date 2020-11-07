from easyaccomod.models import User
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.core import BooleanField, SelectField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from easyaccomod.owner_models import City

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    role = SelectField("Role You Want!", validate_choice=True, validators=[DataRequired()], choices=[('1', 'Renter'), ('2', 'Owner')])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    qry = City.query.all()
    citiest =[]
    for city in qry:
        print(city.name)
        citiest.append(city.name)
    city = SelectField("Choose your City",choices=citiest)
    district = SelectField("Choose your District",choices=None)
    street = SelectField("Choose your Street",choices=None)
    submit = SubmitField("Search")
