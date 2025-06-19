from flask import Flask, render_template, request 
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql


app = Flask(__name__)

if __name__ == '__main__':
    app.run(True)


engine = create_engine("mysql+pymysql://root:Lunanova105@localhost/facturacion02?charset=utf8mb4")

conection = engine.connect()

session = sessionmaker(bind=engine)

session = session()

Base = declarative_base()

Base.metadata.bind = engine



@app.route('/')
def index():
    return render_template('index.html',titulo='inicio')

@app.route('/lista_productos')
def lista_productos():
    try:
        productos = Producto.traer_productos()
        return render_template('lista_productos.html',titulo='lista de productos',productos=productos)
    except: 
            return render_template('lista_productos.html',titulo='Error de conexión a la base de datos')

    

@app.route('/formulario_usuario')
def formulario_usuario():
    return render_template('formulario_usuario.html',titulo='iniciar sesion')



@app.route('/formulario_producto', methods =['GET','POST'])
def formulario_producto():
    categorias = Categoria.traer_categorias()

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        producto_repetido = session.query(Producto).filter(Producto.nombre == nombre).first()  
        producto_repetido = session.query(Producto).filter(Producto.descripcion == descripcion).first()            
        cantidad_inventario = request.form.get('cantidad_inventario')
        precio_unitario = request.form.get('precio_unitario')
        unidad_medida = request.form.get('unidad_medida')
        categoria = request.form.get('categoria')
        producto_almacenar = Producto(nombre,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria)
    
        if producto_repetido:
            return render_template('formulario_producto.html',titulo='error: producto repetido',
                                   errornomb ="el nombre no se puede repetir", errordescr ="la descripcion no se puede repetir"
                                   ,categorias = categorias,producto_almacenar=producto_almacenar)
        try:
            Producto.crear_producto(producto_almacenar) 

        
        except:
            return render_template('formulario_producto.html',titulo='error al registrar en la base de datos')        
    return render_template('formulario_producto.html',titulo='registro de productos',categorias = categorias)


@app.route('/formulario_Nue_usuario')
def formulario_Nue_usuario():
    return render_template('formulario_Nue_usuario.html',titulo='registrarse')

@app.route('/factura')
def factura():
    return render_template('factura.html',titulo='facturacion')

class Producto (Base):
    __tablename__="Producto"
    id_producto = Column(Integer,primary_key=True)
    nombre =Column(String(300), unique=True)
    descripcion =Column(String(300), unique=True)
    cantidad_inventario = Column(Float(10,8))
    precio_unitario = Column(Float(10,8))
    unidad_medida = Column(String(3), nullable =False)
    categoria =Column (Integer,ForeignKey('Categoria.id'), nullable=False)


    def __init__ (self,nombre,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria):
        self.nombre = nombre 
        self.descripcion =  descripcion
        self.cantidad_inventario = cantidad_inventario
        self.precio_unitario = precio_unitario
        self.unidad_medida = unidad_medida
        self.categoria = categoria


    def crear_producto(producto):
        producto = session.add(producto)
        session.commit()
        return producto
    
    def traer_productos():
        productos = session.query(Producto).all()
        return productos
    

class Categoria (Base):
    __tablename__="Categoria"
    id = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(300),unique=True,nullable =False)

     
    def __init__(self, nombre_categoria):
        self.nombre_categoria = nombre_categoria

    def traer_categorias():
        categorias = session.query(Categoria).all()
        return categorias
 


Base.metadata.create_all(engine)  
