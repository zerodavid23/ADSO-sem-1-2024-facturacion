from flask_controller import FlaskController
from flask import render_template, request 
from src.models.productos import Producto
from src.models.categorias import Categoria
from src.app import app


class productosController(FlaskController):
    
    @app.route('/lista_productos')
    def lista_productos():
        try:
            productos = Producto.traer_productos()
            return render_template('lista_productos.html',titulo='lista de productos',productos=productos)
        except: 
                return render_template('lista_productos.html',titulo='Error de conexión a la base de datos')

@app.route('/formulario_producto', methods =['GET','POST'])
def formulario_producto():
    categorias = Categoria.traer_categorias()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        producto_repetido_nombre = Producto.traer_producto_nombre(nombre)
        producto_repetido_descripcion = Producto.traer_producto_descripcion(descripcion)        
        cantidad_inventario = request.form.get('cantidad_inventario')
        precio_unitario = request.form.get('precio_unitario')
        unidad_medida = request.form.get('unidad_medida')
        categoria = request.form.get('categoria')
        producto_almacenar = Producto(nombre,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria)
    #revisar si la instancia funciona con ambas y arroja el recuadro de producto repetido 
        if producto_repetido_descripcion:
            return render_template('formulario_producto.html',titulo='error: producto repetido',
                                    errordescr ="la descripcion no se puede repetir"
                                   ,categorias = categorias,producto_almacenar=producto_almacenar)
        
        #revisar la proxima clase secuencia de logica en la cual se presenta un problema al validar un dato existente y uno no existente que rompe el codigo
        if producto_repetido_nombre:
            return render_template('formulario_producto.html',titulo='error: producto repetido',
                                   errornomb ="el nombre no se puede repetir"
                                   ,categorias = categorias,producto_almacenar=producto_almacenar)
        try:
            Producto.crear_producto(producto_almacenar) 
            

        
        except:
            return render_template('formulario_producto.html',titulo='error al registrar en la base de datos')        
    return render_template('formulario_producto.html',titulo='registro de productos',categorias = categorias)

