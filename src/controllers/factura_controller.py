from flask_controller import FlaskController
from flask import render_template,request, session as flask_session
from src.app import app
from src.models import session as db_session
from src.models.factura import Factura
from src.models.detalle_factura import DetalleFactura
from src.models.productos import Producto
from src.models.usuarios import usuario
from sqlalchemy.orm import joinedload




    
class facturaController(FlaskController):
    @app.route('/factura', methods=['GET', 'POST'])
    def factura():
        if 'productos' not in flask_session:
            flask_session['productos'] = []
        
        if request.method == 'POST':

            # Obtener los datos del formulario
            correo = request.form.get('correo')
            nombre_usuario = request.form.get('nombre_usuario')
            id_producto = request.form.get('id_producto')
            nombre_producto = request.form.get('nombre_producto')
            cantidad_ingresada = request.form.get('cantidad_ingresada')
            fecha = request.form.get('fecha')
            accion = request.form.get('accion')
            print("accion recibida:", accion)

            # Validar los datos
            correo_erroneo = usuario.traer_usuarios_correo(correo)
            if correo_erroneo is None or correo == '':
                return render_template('factura.html', titulo='Error: Correo no encontrado',
                                            errorcorreo="El correo ingresado no está registrado.",
                                            productos=flask_session['productos'])
            usuario_erroneo = usuario.traer_usuarios_usuario(nombre_usuario)
            if usuario_erroneo is None or nombre_usuario == '':
                    return render_template('factura.html', titulo='Errror: usuario no encontrado',
                                        errorusuario="el nombre de usuario ingresado no esta registrado.",
                                            productos=flask_session['productos'])
            id_producto_erroneo = Producto.traer_producto_id(id_producto)
            if id_producto_erroneo is None or id_producto == '':
                    return render_template('factura.html', titulo='Error: Producto no encontrado',
                                        erroridproducto="El ID del producto ingresado no está registrado.",
                                        productos=flask_session['productos'])
            nombre_producto_erroneo = Producto.traer_producto_nombre(nombre_producto)
            if nombre_producto_erroneo is None or nombre_producto == '':
                        return render_template('factura.html', titulo='Error: Producto no encontrado',
                                            errornombreproducto="El nombre del producto ingresado no está registrado.",
                                            productos=flask_session['productos'])
            # Verificar coincidencia exacta del usuario       
            usuario_object = db_session.query(usuario).filter_by(
                correo=correo, nombre_usuario=nombre_usuario).first()
            if not usuario_object:
                    return render_template('factura.html', 
                                        titulo='Error: Usuario no encontrado',
                                        Productos=flask_session['productos'])
                
            #buscar el producto por id y nombre de producto
            producto_object = db_session.query(Producto).filter_by(
                id_producto=id_producto, nombre_producto=nombre_producto).first()

            if not producto_object:
                    return render_template('factura.html', 
                                        titulo='Error: Producto no encontrado',
                                        productos=flask_session['productos'])
            
            # Guardar producto temporalmente en session
            if accion == 'agregar_producto':        
                producto_temp = {
                    'id_producto': id_producto,
                    'nombre_producto': nombre_producto,
                    'cantidad': cantidad_ingresada,
                    'descripcion': producto_object.descripcion if producto_object else '',
                    'fecha': fecha
                }
                flask_session['productos'].append(producto_temp)
                flask_session.modified = True

                return render_template('factura.html',
                                    titulo='Producto agregado',
                                    productos=flask_session['productos'],
                                    mensaje="Producto agregado correctamente.",
                                    #sirve para mantener los datos del formulario
                                    form_data={'correo': correo,
                                               'nombre_usuario': nombre_usuario})
            
            # Crear factura si la acción es 'crear_factura'
            elif accion == 'crear_factura':
                # nueva cabecera de factura
                nueva_cabecera = Factura(  
                      id_usuario=usuario_object.id_usuario,
                      fecha=fecha
                )
                # Guardar la cabecera de la factura
                db_session.add(nueva_cabecera)
                db_session.commit() 
                # Crear detalles de la factura para cada producto en el carrito
                for prod in flask_session['productos']:
                    producto_object = db_session.query(Producto).filter_by(id_producto=prod['id_producto']).first()
                    if producto_object:
                        detalle = DetalleFactura (
                            id_factura=nueva_cabecera.id_factura,
                            id_producto=producto_object.id_producto,
                            cantidad=float(prod['cantidad']),
                            precio_unitario=producto_object.precio_unitario,
                        )
                        db_session.add(detalle)
                db_session.commit()

                # Limpiar el carrito después de crear las facturas
                flask_session['productos'] = []
                flask_session.modified = True

                # Consultar las facturas del usuario para mostrar
            facturas_usuario = db_session.query(Factura)\
                        .options(joinedload(Factura.detalles).joinedload(DetalleFactura.producto_object))\
                        .filter_by(id_usuario=usuario_object.id_usuario)\
                        .all()
            # Calcula el total de la primera factura (o de la que necesites)
            total = sum(det.total for det in facturas_usuario[0].detalles) if facturas_usuario else 0

            return render_template('factura.html',
                                titulo='Factura creada exitosamente',
                                facturas=facturas_usuario,
                                usuario=usuario_object,
                                total=total)        


        return render_template('factura.html',
                            titulo='Factura',
                                productos=flask_session['productos'])


@app.route('/historial_facturas')
def historial_facturas():
    facturas = db_session.query(Factura).all()

    # Cargar detalles y calcular total por cada factura
    facturas_con_total = []
    for factura in facturas:
        total = sum(d.cantidad * float(d.precio_unitario) for d in factura.detalles)
        facturas_con_total.append((factura, total))

    return render_template('historial_facturas.html', facturas=facturas_con_total)


@app.route('/detalle_factura/<int:id_factura>')
def detalle_factura(id_factura):
    session = db_session
    factura = session.query(Factura).get(id_factura)
    detalles = session.query(DetalleFactura).filter_by(id_factura=id_factura).all()
    cliente = session.query(usuario).get(factura.id_usuario)

    total = sum(d.cantidad * float(d.precio_unitario) for d in detalles)

    return render_template('detalle_factura.html',
                           factura=factura,
                           detalles=detalles,
                           cliente=cliente,
                           total=total)
