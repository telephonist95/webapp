from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField, FileField
from wtforms.validators import DataRequired


class BuildingForm(FlaskForm):
    number = IntegerField('Номер корпуса', validators=[DataRequired()])
    floors_count = IntegerField('Количество этажей', validators=[DataRequired()])
    address = StringField('Адрес корпуса', validators=[DataRequired()])
    image = FileField('Картинка фасада')
    submit = SubmitField('Подтвердить')
