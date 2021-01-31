from proyecto import app
from flask import render_template, request, flash, redirect, url_for
import sqlite3
from datetime import date, datetime, time
from proyecto.forms import ReusableForm
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from decimal import *
from requests import Request, Session
from requests.exceptions import ConnectionError , Timeout , TooManyRedirects 
import json
import requests

DBFILE = DBFILE = 'proyecto/data/dbfile.db'
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'
API_KEY= 'ff4f88a1-8c9f-4888-8548-c841771b41a3'

def precioActual(moneda,disponible):
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(1, "EUR", moneda, API_KEY)
    respuesta = requests.get(url)
    dato = respuesta.json()
    precio = (dato['data']['quote'][moneda]['price'])
    return(disponible/precio)

def consulta(query, params=()):
    conn = sqlite3.connect(DBFILE)
    c = conn.cursor()

    c.execute(query, params)
    conn.commit()

    filas = c.fetchall()
    print(filas)

    conn.close()


    if len(filas) == 0:
        return filas

    columnNames = []
    for columnName in c.description:
        columnNames.append(columnName[0])

    listaDeDiccionarios = []

    for fila in filas:
        d = {}
        for ix, columnName in enumerate(columnNames):
            d[columnName] = fila[ix]
        listaDeDiccionarios.append(d)

    return listaDeDiccionarios

@app.route('/')
def listaMovimientos():

    ingresos = consulta('SELECT * FROM transacciones;')

    for transaccion in ingresos:
        precio_u = (transaccion['from_cuantity'])/(transaccion['to_quantity'])
        preciounitario = Decimal(precio_u)
        print(preciounitario)
        transaccion['preciounitario'] = float('{0:.2f}'.format(preciounitario))

    return render_template("listabase.html", datos = ingresos)

@app.route('/compra',  methods=['GET', 'POST'])

def compra():
    form = ReusableForm(request.form)

    wallet = consulta("""SELECT moneda , totalTo - COALESCE(totalFrom,0) as disponible
                        FROM (
                        SELECT to_curency as moneda, totalTo, totalFrom from ((SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) LEFT OUTER JOIN (SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) ON to_curency = from_curency)
                        UNION 
                        SELECT from_curency as moneda, totalTo, totalFrom from ((SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) LEFT OUTER JOIN (SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) ON from_curency = to_curency))""")

    listamonedas =[wallet[i]["moneda"] for i in range(len(wallet))]
    if "EUR" not in listamonedas:
        listamonedas.append("EUR")
    dicMonedas = {wallet[i]["moneda"]:wallet[i]["disponible"] for i in range(len(wallet))}
    print(listamonedas)
    form.MonedaFrom.choices = sorted(listamonedas)
    print(dicMonedas)

    if request.method == "POST":
        if 'Aceptar' not in request.form:
            validCoin = True
            validTo = True
            validAmount = True
            if form.MonedaFrom.data == form.MonedaTo.data:
                validCoin=False
                validTo = False
                flash('Las monedas son iguales.')

            if form.MonedaFrom.data != 'BTC' and form.MonedaTo.data == 'EUR':
                validCoin = False
                validTo = True
                flash('Solo puedes convertir a EUR desde BTC')

            if  form.MonedaFrom.data != "EUR" and (form.CantidadFrom.data > dicMonedas[form.MonedaFrom.data]):
                flash("Insufficient credit, please correct amount of coins to sell")
                validAmount = False
            
            if (not validCoin or not validTo or not validAmount):
                return render_template('purchase.html', form=form, wallet=wallet,validCoin=validCoin, validTo=validTo, validAmount=validAmount, validation=True)
            
            
            url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(1, form.MonedaTo.data, form.MonedaFrom.data, API_KEY)
            respuesta = requests.get(url)
            dato = respuesta.json()
            print(dato)
            precio = (dato['data']['quote'][form.MonedaFrom.data]['price'])
            print(precio)
            preciounitario = round(form.CantidadFrom.data/precio)
            form.CantidadTo.raw_data =[round(form.CantidadFrom.data/precio,8)]
            form.precioUnitario.raw_data = [round(precio,8)]
            
            print(form.CantidadTo.data)
            print(precio)
            return render_template("purchase.html", form=form, wallet=wallet, validAmount=validAmount, validCoin =validCoin, validTo=validTo, validation=True, correct=True)

        else:
            if form.validate():
                today = date.today()
                fecha = today.strftime("%d/%m/%Y")
                hour = datetime.now().time()
                
                consulta('INSERT INTO transacciones (date, time, from_curency, from_cuantity, to_curency, to_quantity) VALUES (?, ? ,?, ? ,?,?);', 
                        (
                            str(fecha),
                            str(hour),
                            form.MonedaFrom.data,
                            form.CantidadFrom.data,
                            form.MonedaTo.data,
                            form.CantidadTo.data
                        )
                )
                
                return redirect(url_for('listaMovimientos'))
            else:
                print(form.MonedaFrom)
                flash(form.CantidadFrom.errors)
                flash('Error:hofdhfd')
    else:
        print(wallet)
        return render_template("purchase.html", form=form, wallet=wallet)
    
@app.route('/status',  methods=['GET', 'POST'])

def status():
    wallet = consulta("""SELECT moneda , COALESCE(totalTo,0) - COALESCE(totalFrom,0) as disponible
                        FROM (
                        SELECT to_curency as moneda, totalTo, totalFrom from ((SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) LEFT OUTER JOIN (SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) ON to_curency = from_curency)
                        UNION 
                        SELECT from_curency as moneda, totalTo, totalFrom from ((SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) LEFT OUTER JOIN (SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) ON from_curency = to_curency))""")


    dicMonedas = {wallet[i]["moneda"]:precioActual(wallet[i]["moneda"],wallet[i]["disponible"]) for i in range(len(wallet))}
    print(dicMonedas)
    inversion= sum(dicMonedas.values())
    print(inversion)
    return render_template("status.html", inversion=round(inversion,2))   