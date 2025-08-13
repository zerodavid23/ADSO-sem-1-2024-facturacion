from flask_controller import FlaskController
from flask import render_template,request, session as flask_session
from src.app import app
from src.models import session as db_session
from src.models.factura import Factura
from src.models.detalle_factura import DetalleFactura
from src.models.productos import Producto
from src.models.usuarios import usuario
from sqlalchemy.orm import joinedload
from datetime import datetime,timezone




    
class facturaController(FlaskController):
    @app.route('/factura', methods=['GET', 'POST'])
    def factura():
        #previsualizador de la factura
        if 'productos' not in flask_session:
            flask_session['productos'] = []
        
        if request.method == 'POST':

            # Obtener los datos del formulario
            correo = request.form.get('correo','').strip()
            nombre_cli = request.form.get('nombre_cli','').strip()
            nombre_usuario = request.form.get('nombre_usuario','').strip()
            id_producto = request.form.get('id_producto','').strip()
            nombre_producto = request.form.get('nombre_producto','').strip()
            cantidad_ingresada = request.form.get('cantidad_ingresada','').strip()
            fecha_str = request.form.get('fecha','').strip()
            accion = request.form.get('accion')
            print("accion recibida:", accion)

            # Validar los datos
            correo_erroneo = usuario.traer_usuarios_correo(correo)
            if correo_erroneo is None or correo == '':
                return render_template('factura.html', titulo='Error: Correo no encontrado',
                                            errorcorreo="El correo ingresado no está registrado.",
                                            productos=flask_session['productos'],
                                            form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario})
            cliente_erroneo = usuario.traer_usuarios_usuario(nombre_cli)
            if cliente_erroneo is None or nombre_cli == '':
                 return render_template('factura.html', titulo='Error: usuario de cliente no encontrado',
                                        errorcliente="el nombre del usuario cliente no esta registrado. ",
                                        productos=flask_session['productos'],
                                        form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario})

            usuario_erroneo = usuario.traer_usuarios_usuario(nombre_usuario)
            if usuario_erroneo is None or nombre_usuario == '':
                    return render_template('factura.html', titulo='Errror: usuario de empleado no encontrado',
                                        errorusuario="el nombre de usuario ingresado no esta registrado.",
                                            productos=flask_session['productos'],
                                            form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario})
            producto_object = None
            if id_producto:
                producto_object= Producto.traer_producto_id(id_producto)
                if producto_object is None:
                    return render_template(
                        'factura.html',
                        titulo='error: producto no encontrado',
                        erroidproducto="el id del producto ingresado no esta registrado",
                        productos=flask_session['productos'],
                        form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario}
                    )
                if nombre_producto and not producto_object:
                    producto_object =Producto.traer_producto_nombre(nombre_producto)
                    if producto_object is None:
                        return render_template(
                            'factura.html',
                            titulo='error:producto no encontrado',
                            errornombreproducto="el nombre del producto ingresado no esta registrado",
                            productos=flask_session['productos'],
                            form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario}
                        )

            # Guardar producto temporalmente en session
            if accion == 'agregar_producto':   
                try:
                    cantidad_val =float(cantidad_ingresada)
                except:
                    cantidad_val = None
                    if not producto_object or cantidad_val  is None:
                        return render_template(
                            'factura.html',
                            titulo='error al agregar producto',
                            mensaje='producto o cantidad invalida',
                            productos =flask_session['productos'],
                            form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario}

                        )
                producto_temp = {
                    'id_producto': int(producto_object.id_producto),
                    'nombre_producto': producto_object.nombre_producto,
                    'cantidad': cantidad_val,
                    'descripcion': producto_object.descripcion,
                    'fecha': fecha_str or None
                }
                flask_session['productos'].append(producto_temp)
                flask_session.modified = True

                return render_template(
                    'factura.html',
                    titulo='Producto agregado',
                    mensaje="Producto agregado correctamente.",
                    form_data={
                        'correo': correo,
                        'nombre_cli': nombre_cli,
                        'nombre_usuario': nombre_usuario},
                    productos=flask_session['productos']
                )
            
            # Crear factura si la acción es 'crear_factura'
            elif accion == 'crear_factura':
                prod_to_add = None
                # nueva cabecera de factura
                if id_producto and nombre_producto:
                    if not any(str(p['id_producto']) == str(id_producto)for p in flask_session['productos']):
                        try:
                            cantidad_val = float(cantidad_ingresada)
                        except:
                            cantidad_val = 0.0
                        prod_to_add = {
                                'id_producto': int(id_producto),
                                'nombre_producto': nombre_producto,
                                'cantidad': cantidad_val,
                                'descripcion': producto_object.descripcion if producto_object else '',
                                'fecha': fecha_str or None
                        }
                if prod_to_add:
                # Limpiar el carrito después de crear las facturas
                    flask_session['productos'].append(prod_to_add)
                    flask_session.modified = True
                
            usuario_empleado = db_session.query(usuario).filter_by(
                correo = correo,
                nombre_usuario=nombre_usuario
            ).first()
            usuario_cliente = db_session.query(usuario).filter_by(
                nombre_usuario=nombre_cli
            ).first()
            if not usuario_empleado or not usuario_cliente:
                return render_template(
                    'factura.html',
                    titulo='error usuario no valido',
                    errorusuario='empleado o cliente invalido',
                    productos=flask_session['productos'],
                    form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario}
                )
            if fecha_str:
                try:
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
                except Exception:
                    fecha_obj = datetime.now(timezone.utc)
                else:
                    fecha_obj =datetime.now(timezone.utc)

                nueva_cabecera = Factura(
                    id_empleado=usuario_empleado.id_usuario,
                    id_cliente=usuario_cliente.id_usuario,
                    fecha=fecha_obj
                )
                db_session.add(nueva_cabecera)
                db_session.commit()  # para obtener id_factura      

                for prod in flask_session['productos']:
                    prod_row = db_session.get(Producto, int(prod['id_producto']))
                    precio_unit = float(prod_row.precio_unitario) if prod_row and prod_row.precio_unitario is not None else 0.0

                    detalle = DetalleFactura(
                        id_factura= nueva_cabecera.id_factura,
                        id_producto= int(prod['id_producto']),
                        cantidad=float(prod['cantidad']),
                        precio_unitario=precio_unit

                    )
                    db_session.add(detalle)
                    db_session.commit()

                    factura_creada = db_session.query(Factura)\
                    .options(joinedload(Factura.detalles).joinedload(DetalleFactura.producto_object))\
                    .get(nueva_cabecera.id_factura)

                    total =sum(float(det.cantidad) * float (det.precio_unitario) for det in factura_creada.detalles)

                    flask_session['productos'] = []
                    flask_session.modified = True
                # Consultar las facturas del usuario para mostrar
          

                return render_template('factura.html',
                                    titulo='factura creada',
                                        facturas=[factura_creada],
                                        usuario=usuario_cliente,
                                        empleado=usuario_empleado,
                                        total=total)

            return render_template(
                            'factura.html',
                            titulo='Facturacion',
                            productos=flask_session['productos'],
                            form_data={'correo': correo, 'nombre_cli': nombre_cli, 'nombre_usuario': nombre_usuario}
                        )
        return render_template('factura.html',
                                titulo='Facturacion',
                                productos=flask_session.get('productos', []))

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
    cliente = session.query(usuario).get(factura.id_cliente)
    empleado = session.query(usuario).get(factura.id_empleado) if hasattr(factura, 'id_empleado') else None

    total = sum(d.cantidad * float(d.precio_unitario) for d in detalles)

    return render_template('detalle_factura.html',
                            factura=factura,
                            cliente=cliente,
                            empleado=empleado,
                            detalles=detalles,
                            total=total)