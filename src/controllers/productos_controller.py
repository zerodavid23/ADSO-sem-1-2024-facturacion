from flask_controller import FlaskController
from flask import render_template, request, redirect, url_for,flash,abort
from  sqlalchemy import func
from src.models.productos import Producto
from src.models.categorias import Categoria
from src.models import session as db_session
from src.app import app


class productosController(FlaskController):
    
    @app.route('/lista_productos')
    def lista_productos():
        try:
            productos = Producto.traer_productos()
            return render_template('lista_productos.html',titulo='lista de productos',productos=productos)
        except: 
                return render_template('lista_productos.html',titulo='Error de conexión a la base de datos')

@app.route('/formulario_producto', methods=['GET','POST'])
@app.route('/formulario_producto/<int:id_producto>', methods=['GET','POST'])
def formulario_producto(id_producto=None):
   
    categorias = Categoria.traer_categorias()
    producto = None

    # Si llega id en la URL, cargar producto (GET o POST)
    if id_producto is not None:
        producto = db_session.get(Producto, id_producto)
        if producto is None:
            flash('Producto no encontrado', 'danger')
          
            return redirect(url_for('lista_productos'))

    #  crear o actualizar los productos
    if request.method == 'POST':
        nombre = (request.form.get('nombre') or '').strip()
        descripcion = (request.form.get('descripcion') or '').strip()
        cantidad = request.form.get('cantidad_inventario')
        precio = request.form.get('precio_unitario')
        unidad_medida = (request.form.get('unidad_medida') or '').strip()
        categoria_id = request.form.get('categoria') or None

        
        if not nombre:
            flash('El nombre es obligatorio', 'danger')
            return redirect(request.url)   
        try:
            cantidad_val = float(cantidad) if cantidad not in (None, '') else None
        except ValueError:
            flash('Cantidad inválida', 'danger')
            return redirect(request.url)

        try:
            precio_val = float(precio) if precio not in (None, '') else None
        except ValueError:
            flash('Precio inválido', 'danger')
            return redirect(request.url)

        # Actualizar el producto 
        if producto:
            producto.nombre_producto = nombre
            producto.descripcion = descripcion
            producto.cantidad_inventario = cantidad_val if cantidad_val is not None else producto.cantidad_inventario
            producto.precio_unitario = precio_val if precio_val is not None else producto.precio_unitario
            producto.unidad_medida = unidad_medida
            producto.categoria = int(categoria_id) if categoria_id else producto.categoria
            try:
                db_session.commit()
                flash('Producto actualizado', 'success')
                return redirect(url_for('lista_productos'))
            except Exception as e:
                db_session.rollback()
                flash(f'Error al actualizar: {e}', 'danger')
                return redirect(request.url)

        # Crear nuevo
        nuevo = Producto(nombre, descripcion, cantidad_val or 0.0, precio_val or 0.0, unidad_medida, int(categoria_id) if categoria_id else None)
        try:
            Producto.crear_producto(nuevo)
            flash('Producto creado', 'success')
            return redirect(url_for('lista_productos'))
        except Exception as e:
            # si crear_producto no hace commit, protege con rollback
            try:
                db_session.rollback()
            except: pass
            flash(f'Error al crear producto: {e}', 'danger')
            return redirect(request.url)


    return render_template('formulario_producto.html', producto=producto, categorias=categorias)