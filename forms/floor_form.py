from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, FileField
from wtforms.validators import DataRequired


class FloorForm(FlaskForm):
    number = IntegerField('Номер этажа', validators=[DataRequired()])
    rooms_count = IntegerField('Количество кабинетов', validators=[DataRequired()])
    image = FileField('Картинка этажа')
    rooms_coords = StringField('Координаты комнат')
    submit = SubmitField('Подтвердить')
