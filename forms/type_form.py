from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class TypeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
