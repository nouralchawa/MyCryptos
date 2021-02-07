from flask_wtf import FlaskForm
from wtforms import SelectField, TextField, SubmitField, TextAreaField, IntegerField, FloatField, StringField, Form, DateTimeField
from wtforms.validators import Length, Required, NumberRange
import datetime

mismonedas =('EUR','BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'BNB', 'USDT', 'EOS', 'BSV', 'XLM', 'ADA', 'TRX')



class ReusableForm(Form):

        
        #timeofOp = DateTimeField('Time of Operation',
        #                      format='%Y-%m-%d %H:%M:%S')
        timeofOp = StringField("Time of Operation")
        MonedaFrom = SelectField('From:', validators=[Required()] )
        CantidadFrom = FloatField('Quantity:', validators=[Required() ])
        MonedaTo = SelectField('To:', choices= mismonedas, validators=[Required()] )
        CantidadTo = FloatField('Quantity:', validators=[])
        precioUnitario = FloatField('P.U.:', validators=[])

        Calculadora = SubmitField('Calculadora')
        Aceptar = SubmitField('SUBMIT')


