
from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.core import BooleanField, IntegerField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=10, max= 99)])
    content = TextAreaField("Content", validators=[DataRequired()])
    room_id = IntegerField("Room ID", validators=[DataRequired()])
    pending = BooleanField("Pending", validators=[DataRequired()])
    submit = SubmitField("Post")

