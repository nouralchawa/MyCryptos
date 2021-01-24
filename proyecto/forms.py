from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, SubmitField, TextAreaField, IntegerField, FloatField, StringField
from wtforms.validators import Length, Required

mismonedas =('EUR','BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX')

class QuizForm(FlaskForm):
        MonedaFrom = SelectField('From', choices= mismonedas, validators=[Required()] )
        CantidadFrom = FloatField('CantidadFrom', validators=[Required()])
        MonedaTo = SelectField('To', choices= mismonedas, validators=[Required()] )
        CantidadTo = FloatField('CantidadTo', validators=[Required()])

        Calculadora = SubmitField('Calculadora')
        Aceptar = SubmitField('Aceptar')

