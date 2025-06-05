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
    return render_template('lista_productos.html',titulo='lista de productos')

@app.route('/formulario_usuario')
def formulario_usuario():
    return render_template('formulario_usuario.html',titulo='iniciar sesion')



@app.route('/formulario_producto', methods =['GET','POST'])
def formulario_producto():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        cantidad_inventario = request.form.get('cantidad_inventario')
        precio_unitario = request.form.get('precio_unitario')
        unidad_medida = request.form.get('unidad_medida')
        categoria = request.form.get('categoria')
        
        producto = Producto(nombre,descripcion,cantidad_inventario,precio_unitario,unidad_medida,categoria)
        Producto.crear_producto(producto) 
         

    return render_template('formulario_producto.html',titulo='registro de productos')


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
    

class Categoria (Base):
     __tablename__="Categoria"
     id = Column(Integer, primary_key=True)
     nombre_categoria = Column(String(300),unique=True,nullable =False)

Base.metadata.create_all(engine)  
