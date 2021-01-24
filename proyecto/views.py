from proyecto import app
from flask import render_template, request, flash
import sqlite3
from datetime import date
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

DBFILE = DBFILE = 'proyecto/data/dbfile.db'
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required(message="El concepto debe tener más de 10 caracteres")]) 

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

    ingresos = consulta('SELECT date, time, from_curency, from_cuantity, to_curency, to_quantity, id FROM transacciones;')

    return render_template("listabase.html")

@app.route('/compra',  methods=['GET', 'POST'])

def compra():
    form = ReusableForm(request.form)
    '''
    if request.method == 'POST':
        name=request.form['name']


        if form.validate():
            write_to_disk(name)
            flash('Hello: {}'.format(name))

        else:
            flash('Error: All Fields are Required')

    return render_template("purchase.html", form = form)
    
    '''
    
    if request.method == 'POST':
        if form.validate():
            today = date.today()
            fecha = today.strftime("%d/%m/%Y")
            hour = datetime.now().time()
            '''
            consulta('INSERT INTO transacciones (date, time, from_curency, from_cuantity, to_curency, to_quantity) VALUES (?, ? ,?, ? );', 
                    (
                        str(fecha),
                        str(hour),
                        form.MonedaFrom.data,
                        form.CantidadFrom.data,
                        form.MonedaTo.data,
                        form.CantidadTo.data
                    )
            )
            '''
            return redirect(url_for('listabase.html'))
        else:
            flash('Error:hofdhfd')
            

    return render_template("purchase.html", form=form)
    
    