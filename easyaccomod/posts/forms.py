
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
    room_type_query = RoomType.query.all()
    bathroom_type_query = BathroomType.query.all()
    kitchen_type_query = KitchenType.query.all()
    room_types = []
    bathroom_types = []
    kitchen_types = []
    for rt in room_type_query:
        room_types.append((rt.id, rt.name))
    for bt in bathroom_type_query:
        bathroom_types.append((bt.id, bt.name))
    for kt in kitchen_type_query:
        kitchen_types.append((kt.id, kt.name))

    city = SelectField("City", validate_choice=False ,validators=[DataRequired()])
    district = SelectField("District",validate_choice=False ,validators=[DataRequired()])
    ward = SelectField("Ward", validate_choice=False,validators=[DataRequired()])
    info = StringField("Info", validators=[DataRequired(), Length(min=10, max=120)])
    room_type = SelectField("Kiểu Phòng", validate_choice=True, choices=room_types, validators=[DataRequired()])
    room_number = IntegerField("Số Phòng", validators=[DataRequired()])
    price = IntegerField("Giá Thuê phòng", validators=[DataRequired()], render_kw={"placeholder": "VND/tháng"})
    dien_tich = IntegerField("Diện tích", validators=[DataRequired()], render_kw={"placeholder": "m2"})
    chung_chu = BooleanField("Chung Chủ")
    phong_tam = IntegerField("Phòng Tắm", validators=[DataRequired()])
    loai_phong_tam = SelectField("Loại Phòng Tắm", validate_choice=True, choices=bathroom_types, validators=[DataRequired()])
    nong_lanh = BooleanField("Nóng Lạnh")
    phong_bep = IntegerField("Phòng Bếp", validators=[DataRequired()])
    loai_phong_bep = SelectField("Loại Phòng Bếp", validate_choice=True, choices=kitchen_types, validators=[DataRequired()])
    dieu_hoa = BooleanField("Điều Hòa")
    ban_cong = BooleanField("Ban Công")
    gia_dien = IntegerField("Giá Điện", validators=[DataRequired("This Field is required and be integer!")], render_kw={"placeholder": "VND/số"})
    gia_nuoc = IntegerField("Giá Nước", validators=[DataRequired("This Field is required and be integer!")], render_kw={"placeholder": "VND/khối"})
    tien_ich_khac = TextAreaField("Tiện ích khác")
    image = MultipleFileField("Image", validators=[DataRequired(), FileAllowed(['jpg', 'jpeg', 'png'])])
    status = BooleanField("Status")
    submit = SubmitField("Post Room")

    def validate_image(self, image):
        if len(image.data) < 3:
            raise ValidationError('Min 3 files')