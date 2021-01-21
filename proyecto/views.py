from proyecto import app
from flask import render_template


@app.route('/')
def listaMovimientos():
    return render_template("listabase.html")

@app.route('/compra',  methods=['GET', 'POST'])
def compra():
    return render_template("purchase.html")
    
