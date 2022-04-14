from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


class ItemForm(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    type = SelectField('Тип', validators=[DataRequired()])
    count = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
