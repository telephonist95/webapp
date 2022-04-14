from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    number = IntegerField('Номер кабинета', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
