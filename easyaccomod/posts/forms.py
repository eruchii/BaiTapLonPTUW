
from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.core import BooleanField, DateField, IntegerField, SelectField
from flask_wtf.file import FileAllowed
from wtforms import MultipleFileField
from wtforms.validators import DataRequired, Length, ValidationError
from easyaccomod.owner_models import *

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=10, max= 99)])
    content = TextAreaField("Content", validators=[DataRequired()])
    room_id = IntegerField("Room ID", validators=[DataRequired()])
    date_out = DateField("Date Out", validators=[DataRequired()], render_kw={"placeholder": "YYYY-mm-dd"})
    pending = BooleanField("Pending")
    submit = SubmitField("Post")

class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=10, max= 99)])
    content = TextAreaField("Content", validators=[DataRequired()])
    room_id = IntegerField("Room ID", validators=[DataRequired()])
    date_posted = DateField("Date Posted", validators=[DataRequired()], render_kw={"placeholder": "YYYY-mm-dd"})
    date_out = DateField("Date Out", validators=[DataRequired()], render_kw={"placeholder": "YYYY-mm-dd"})
    pending = BooleanField("Pending")
    submit = SubmitField("Update")

class RoomForm(FlaskForm):
    # city_query = City.query.all()
    # cities = []
    # for city in city_query:
    #     cities.append((city.code, city.name))
    # district_query = District.query.all()
    # districts = []
    # for district in district_query:
    #     districts.append((district.id, district.name))
    # ward_query = Ward.query.all()
    # wards = []
    # for ward in ward_query:
    #     wards.append((ward.id, ward.name))
    
    # city = SelectField("City", choices=cities, validators=[DataRequired()])
    # district = SelectField("District", choices=districts, validators=[DataRequired()])
    # ward = SelectField("Ward", choices=wards, validators=[DataRequired()])
    city = SelectField("City", validate_choice=False ,validators=[DataRequired()])
    district = SelectField("District",validate_choice=False ,validators=[DataRequired()])
    ward = SelectField("Ward", validate_choice=False,validators=[DataRequired()])
    info = StringField("Info", validators=[DataRequired(), Length(min=10, max=120)])
    room_type = SelectField("Room Type", validate_choice=True, choices=[('1', 'Phòng trọ'), ('2', 'Chung cư mini'), ('3', 'Nhà nguyên căn'), ('4', 'Chung cư nguyên căn')], validators=[DataRequired()])
    room_number = IntegerField("Room Number", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    chung_chu = BooleanField("Chung Chu")
    phong_tam = IntegerField("Phong Tam", validators=[DataRequired()])
    nong_lanh = BooleanField("Nong Lanh")
    phong_bep = IntegerField("Phong Bep", validators=[DataRequired()])
    dieu_hoa = BooleanField("Dieu Hoa")
    ban_cong = BooleanField("Ban Cong")
    gia_dien = IntegerField("Gia Dien", validators=[DataRequired("This Field is required and be integer!")], render_kw={"placeholder": "VND/số"})
    gia_nuoc = IntegerField("Gia Nuoc", validators=[DataRequired("This Field is required and be integer!")], render_kw={"placeholder": "VND/khối"}) # !need fix int to str
    tien_ich_khac = TextAreaField("Tien ich khac")
    image = MultipleFileField("Image", validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    status = BooleanField("status")
    submit = SubmitField("Post Room")

    def validate_image(self, image):
        if len(image.data) < 3:
            raise ValidationError('min 3 files')