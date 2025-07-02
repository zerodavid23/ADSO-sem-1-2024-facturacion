
from flask_controller import FlaskController
from flask import render_template
from src.app import app

@app.route('/factura')
def factura():
    return render_template('factura.html',titulo='facturacion')
