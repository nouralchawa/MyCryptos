from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea, Select


class MovementForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired()])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=10, message="El concepto debe tener más de 10 caracteres")])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])

    submit = SubmitField('Aceptar')