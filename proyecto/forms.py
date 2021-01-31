from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, SubmitField, TextAreaField, IntegerField, FloatField, StringField, Form
from wtforms.validators import Length, Required, NumberRange


mismonedas =('EUR','BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX')

DBFILE = DBFILE = 'proyecto/data/dbfile.db'


class ReusableForm(Form):
        minimo = 0
        maximo = 1e6
        MonedaFrom = SelectField('From:', validators=[Required()] )
        CantidadFrom = FloatField('Cantidad From:', validators=[Required(), NumberRange(minimo,maximo,"saldo insuficiente") ])
        MonedaTo = SelectField('To:', choices= mismonedas, validators=[Required()] )
        CantidadTo = FloatField('Cantidad To:', validators=[])
        precioUnitario = FloatField('P.U.:', validators=[])

        Calculadora = SubmitField('Calculadora')
        Aceptar = SubmitField('Aceptar')

