from flask import Flask, render_template

app = Flask(__name__)

if __name__ == 'main':
    app.run(True)

@app.route('/')
def index():
    return render_template('index.html',titulo='inicio')

@app.route('/lista_productos')
def lista_productos():
    return render_template('lista_productos.html',titulo='lista de productos')

@app.route('/formulario_usuario')
def formulario_usuario():
    return render_template('formulario_usuario.html',titulo='iniciar sesion')

@app.route('/formulario_producto')
def formulario_producto():
    return render_template('formulario_producto.html',titulo='registro de productos')

@app.route('/formulario_Nue_usuario')
def formulario_Nue_usuario():
    return render_template('formulario_Nue_usuario.html',titulo='registrarse')

@app.route('/factura')
def factura():
    return render_template('factura.html',titulo='facturacion')
