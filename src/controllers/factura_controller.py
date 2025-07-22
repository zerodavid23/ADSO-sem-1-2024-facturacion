
from flask_controller import FlaskController
from flask import render_template,request, session
from src.app import app
from src.models import session
from src.models.factura import Factura
from src.models.productos import Producto
from src.models.usuarios import usuario




class facturaController(FlaskController):
    
    @app.route('/factura', methods=['GET', 'POST'])
    def factura():

        
        if request.method == 'POST':
            # Obtener los datos del formulario
            correo = request.form.get('correo')
            nombre_usuario = request.form.get('nombre_usuario')
            id_producto = request.form.get('id_producto')
            nombre_producto = request.form.get('nombre_producto')
            cantidad_ingresada = request.form.get('cantidad_ingresada')
            fecha = request.form.get('fecha')
            # Validar los datos

            usuario_object = session.query(usuario).filter_by(correo=correo, nombre_usuario=nombre_usuario).first()
            if not usuario_object:
                return render_template('factura.html', titulo='Error: Usuario no encontrado')
            
           

            producto_object = session.query(Producto).filter_by(id_producto=id_producto, nombre_producto=nombre_producto).first()

            if not producto_object:
                return render_template('factura.html', titulo='Error: Producto no encontrado')
            
            factura_nueva = Factura(
                id_usuario=usuario_object.id_usuario,
                id_producto=producto_object.id_producto,
                cantidad_ingresada=float(cantidad_ingresada),
                fecha=fecha
            )
            try:
                Factura.crear_factura(factura_nueva)
                return render_template('factura.html', titulo='Factura creada con éxito')
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