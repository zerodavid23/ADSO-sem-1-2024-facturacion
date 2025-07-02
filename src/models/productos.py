from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import session, Base
from src.models.categorias import Categoria

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
    
    def traer_producto_descripcion(descripcion):
        producto = session.query(Producto).filter(Producto.descripcion == descripcion).first()    
        return producto
    def traer_producto_nombre(nombre):
        producto=session.query(Producto).filter(Producto.nombre == nombre).first()  
        return producto    