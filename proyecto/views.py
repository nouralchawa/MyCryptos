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

DBFILE = app.config['DBFILE']
SECRET_KEY = app.config['SECRET_KEY']
API_KEY= app.config['API_KEY']

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
def start():
    return render_template('mycrypto.html')

@app.route('/index')
def listaMovimientos():
    form = ReusableForm(request.form)

    try:
        ingresos = consulta('SELECT * FROM transacciones;')
    except:
        flash('Unable to connect to the Database. Try later')
        return render_template('error.html', form=form)
    
    for transaccion in ingresos:
        precio_u = (transaccion['from_cuantity'])/(transaccion['to_quantity'])
        preciounitario = Decimal(precio_u)
        print(preciounitario)
        transaccion['preciounitario'] = float('{0:.2f}'.format(preciounitario))

    return render_template("listabase.html", datos = ingresos)

@app.route('/compra',  methods=['GET', 'POST'])

def compra():
    form = ReusableForm(request.form)

    try:
        wallet = consulta("""SELECT moneda , totalTo - COALESCE(totalFrom,0) as disponible
                            FROM (
                            SELECT to_curency as moneda, totalTo, totalFrom from ((SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) LEFT OUTER JOIN (SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) ON to_curency = from_curency)
                            UNION 
                            SELECT from_curency as moneda, totalTo, totalFrom from ((SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) LEFT OUTER JOIN (SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) ON from_curency = to_curency))""")
    except:
        flash('Unable to connect to the Database. Try later')
        return render_template('purchase.html', form=form)

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
                flash('The coins cannot be the same')

            if form.MonedaFrom.data != 'BTC' and form.MonedaTo.data == 'EUR':
                validCoin = False
                validTo = True
                flash('You can only convert to EUR from BTC')

            if  form.MonedaFrom.data != "EUR" and (form.CantidadFrom.data > dicMonedas[form.MonedaFrom.data]):
                flash("Insufficient credit, please correct amount of coins to sell")
                validAmount = False
            
            if (not validCoin or not validTo or not validAmount):
                return render_template('purchase.html', form=form, wallet=wallet,validCoin=validCoin, validTo=validTo, validAmount=validAmount, validation=True)
            
            
            url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(1, form.MonedaTo.data, form.MonedaFrom.data, API_KEY)
            respuesta = requests.get(url)
            if respuesta.status_code ==200:
                dato = respuesta.json()
                print(dato)
                precio = (dato['data']['quote'][form.MonedaFrom.data]['price'])
                print(precio)
                preciounitario = round(form.CantidadFrom.data/precio)
                form.CantidadTo.raw_data =[round(form.CantidadFrom.data/precio,8)]
                form.precioUnitario.raw_data = [round(precio,8)]
                
                print(form.CantidadTo.data)
                print(precio)
                form.MonedaFrom.default = form.MonedaFrom.data
                print(form.MonedaFrom.default)
                form.timeofOp.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("hol!a")
                print(form.timeofOp.data)
                form.MonedaFrom.choices = [form.MonedaFrom.data]
                form.MonedaTo.choices = [form.MonedaTo.data]
                return render_template("purchase.html", form=form, wallet=wallet, validAmount=validAmount, validCoin =validCoin, validTo=validTo, validation=True, correct=True, freeze=True)
            else:
                flash('Error Connecting to coinmarketcap. Try Later')
                return render_template('purchase.html', form=form)
        else:
            
            print("default")
            print(form.MonedaFrom.default)
            print("data")
            print(form.MonedaFrom.data)
            currentTime = datetime.now()
            print(currentTime)
            timeofOp= datetime.strptime(form.timeofOp.data,'%Y-%m-%d %H:%M:%S')
            print(request.form)
            print(form.timeofOp.data)
            difference = currentTime - timeofOp
            print(difference)
            seconds_in_day = 24 * 60 * 60
            timeDifference = divmod(difference.days * seconds_in_day + difference.seconds, 60)
            print(timeDifference[0])
            print(form.validate())
            if timeDifference[0] < 1:
                
                print(form.MonedaFrom.data)
                today = date.today()
                fecha = today.strftime("%d/%m/%Y")
                hour = datetime.now().time()
                
                try:
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

                except:
                    
                    flash('Unable to connect to the Database. Try later')
                    return render_template('purchase.html', form=form)

            else:
                print(form.MonedaFrom)
                #flash(form.CantidadFrom.errors)
                if timeDifference[0] >= 1:
                    flash("Confirmation time expired: press calculator again and submit.")
                return render_template('purchase.html', form=form)    
                
    else:
        print(wallet)
        return render_template("purchase.html", form=form, wallet=wallet)
    
@app.route('/status',  methods=['GET', 'POST'])

def status():
    form = ReusableForm(request.form)
    
    try:
        wallet = consulta("""SELECT moneda , COALESCE(totalTo,0) - COALESCE(totalFrom,0) as disponible
                            FROM (
                            SELECT to_curency as moneda, totalTo, totalFrom from ((SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) LEFT OUTER JOIN (SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) ON to_curency = from_curency)
                            UNION 
                            SELECT from_curency as moneda, totalTo, totalFrom from ((SELECT  from_curency, sum(from_cuantity) as totalFrom FROM transacciones GROUP BY from_curency) LEFT OUTER JOIN (SELECT  to_curency, sum(to_quantity) as totalTo FROM transacciones GROUP BY to_curency) ON from_curency = to_curency))""")
    except:
        flash('Unable to connect to the Database. Try later')
        return render_template('error.html', form=form)

    divisas = "BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX"
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={}&convert={}&CMC_PRO_API_KEY={}'.format(divisas, "EUR", API_KEY)
    respuesta = requests.get(url)
    if respuesta.status_code ==200:
        dato = respuesta.json()
        print(dato['data']["BTC"]['quote']['EUR']['price'])
    
    
        dicMonedas = {wallet[i]["moneda"]:(dato['data'][wallet[i]["moneda"]]['quote']['EUR']['price'] if wallet[i]["moneda"]!="EUR" else 1)*wallet[i]["disponible"] for i in range(len(wallet))}
    #dicMonedas = {wallet[i]["moneda"]:precioActual(wallet[i]["moneda"],wallet[i]["disponible"]) for i in range(len(wallet))}

    #print(dicMonedas)
        inversion= sum(dicMonedas.values())
    #print(inversion)
        return render_template("status.html", inversion=round(inversion,2), eurosinvertidos=-round(dicMonedas['EUR']))   
    else:
        flash('Unable to connect to the coinmarket. Try later')
        return render_template('error.html', form=form)
