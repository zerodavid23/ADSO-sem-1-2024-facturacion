from flask_controller import FlaskController
from flask import render_template,request, session
from src.app import app
from src.models import session
from src.models.factura import Factura
from src.models.productos import Producto
from src.models.usuarios import usuario
from sqlalchemy.orm import joinedload



class facturaController(FlaskController):
    
    @app.route('/factura', methods=['GET', 'POST'])
    def factura():
        if 'productos' not in session:
            session['productos'] = []
        
        if request.method == 'POST':
            # Obtener los datos del formulario
            correo = request.form.get('correo')
            correo_erroneo = usuario.traer_usuarios_correo(correo)
          
            nombre_usuario = request.form.get('nombre_usuario')
            usuario_erroneo = usuario.traer_usuarios_usuario(nombre_usuario)
            id_producto = request.form.get('id_producto')
            id_producto_erroneo = Producto.traer_producto_id(id_producto)
            nombre_producto = request.form.get('nombre_producto')
            nombre_producto_erroneo = Producto.traer_producto_nombre(nombre_producto)
            cantidad_ingresada = request.form.get('cantidad_ingresada')
            fecha = request.form.get('fecha')
            # Validar los datos
            
            if correo_erroneo is None or correo == '':

                return render_template('factura.html', titulo='Error: Correo no encontrado',
                                       errorcorreo="El correo ingresado no está registrado."
                                       productodos=session['productos'])
            if usuario_erroneo is None or nombre_usuario == '':
                return render_template('factura.html', titulo='Errror: usuario no encontrado',
                                       errorusuario="el nombre de usuario ingresado no esta registrado."
                                        productodos=session['productos'])
            if id_producto_erroneo is None or id_producto == '':
                return render_template('factura.html', titulo='Error: Producto no encontrado',
                                       erroridproducto="El ID del producto ingresado no está registrado."
                                       productodos=session['productos'])
            if nombre_producto_erroneo is None or nombre_producto == '':
                return render_template('factura.html', titulo='Error: Producto no encontrado',
                                       errornombreproducto="El nombre del producto ingresado no está registrado."
                                       productodos=session['productos'])
            

            #buscar el usuario por correo y nombre de usuario
            usuario_object = session.query(usuario).filter_by(correo=correo, nombre_usuario=nombre_usuario).first()
            if not usuario_object:
                return render_template('factura.html', titulo='Error: Usuario no encontrado',
                                       Productos=session['productos'])
            
           
            #buscar el producto por id y nombre de producto
            producto_object = session.query(Producto).filter_by(id_producto=id_producto, nombre_producto=nombre_producto).first()

            if not producto_object:
                return render_template('factura.html', titulo='Error: Producto no encontrado',
                                       productos=session['productos'])
            
          
           # Guardar producto temporalmente en session
            producto_temp = {
                'id_producto': id_producto,
                'nombre_producto': nombre_producto,
                'cantidad': cantidad_ingresada,
                'descripcion': producto_object.descripcion if producto_object else'',
                'fecha': fecha
            }
            session['productos'].append(producto_temp)
            session.modified = True

            return render_template('factura.html',
                                   titulo='Producto agregado',
                                   productos=session['productos'],
                                   mensaje="Producto agregado correctamente.")
        
        if request.form.get('accion') == 'crear_factura':
            usuario_object = session.query(usuario).filter_by(correo=correo, nombre_usuario=nombre_usuario).first()
            if not usuario_object:
                return render_template('factura.html', titulo='Error: Usuario no encontrado',
                                       productos=session['productos'])

            # Recorrer productos en el carrito y crear una factura por cada uno
            for prod in session['productos']:
                producto_object = session.query(Producto).filter_by(id_producto=prod['id_producto']).first()
                if producto_object:
                    factura_nueva = Factura(
                        id_usuario=usuario_object.id_usuario,
                        id_producto=producto_object.id_producto,
                        cantidad_ingresada=float(prod['cantidad']),
                        fecha=prod['fecha']
                    )
                    Factura.crear_factura(factura_nueva)

            # Limpiar el carrito después de crear las facturas
            session['productos'] = []
            session.modified = True

            facturas_usuario = session.query(Factura)\
                .options(joinedload(Factura.producto_object))\
                .filter_by(id_usuario=usuario_object.id_usuario)\
                .all()

            return render_template('factura.html', titulo='Factura creada exitosamente', facturas=facturas_usuario, usuario=usuario_object)
        
            #crear y almacenar la factura
            factura_nueva = Factura(
                id_usuario=usuario_object.id_usuario,
                id_producto=producto_object.id_producto,
                cantidad_ingresada=float(cantidad_ingresada),
                fecha=fecha
            )
            try:
                Factura.crear_factura(factura_nueva)
                facturas_usuario = session.query(Factura)\
                .options(joinedload(Factura.producto_object))\
                .filter_by(id_usuario=usuario_object.id_usuario)\
                .all()
                for f in facturas_usuario:
                    print(f"Factura ID: {f.id_factura}, Total: {f.total}")
    
                return render_template('factura.html',titulo='Factura creada exitosamente',facturas=facturas_usuario,usuario=usuario_object)
               
               
            except Exception as e:
                print(f"Error al crear factura: {e}")

                return render_template('factura.html', titulo='Error al crear factura')
            #manejo de errores

           
        return render_template('factura.html',titulo='facturacion')


    @app.route('/historial_facturas')
    def historial_facturas():
        try:
            facturas = Factura.traer_facturas()
            return render_template('historial_facturas.html', titulo='Historial de Facturas', facturas=facturas)
        except:

            return render_template('historial_facturas.html', titulo='error de conexión a la base de datos')

    @app.route('/detalle_factura/<int:id_factura>')
    def detalle_factura(id_factura):
        session = session()

        factura = session.query(Factura).get(id_factura)
        detalles = session.query(DetalleFactura).filter_by(id_factura=id_factura).all()
        cliente = session.query(usuario).get(factura.id_usuario)    

        return render_template('detalle_factura.html', factura=factura, detalles=detalles, cliente=cliente)