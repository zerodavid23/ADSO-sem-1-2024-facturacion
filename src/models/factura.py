from src.models import session, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime


class Factura(Base):
    __tablename__ = "factura"
    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), nullable=False)
    cantidad_ingresada = Column(Float(10,8), nullable=False)
    fecha = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
  
    producto_object = relationship('Producto', back_populates='facturas')
    usuario_object = relationship('usuario', back_populates='facturas')
   
    

   

    def __init__(self,id_usuario, id_producto, cantidad_ingresada, fecha):
        self.id_usuario = id_usuario
        self.id_producto = id_producto
        self.cantidad_ingresada = cantidad_ingresada    
        self.fecha = fecha
   
    @staticmethod   
    def crear_factura(factura):
        session.add(factura)
        session.commit()
        return factura
    @staticmethod 
    def traer_facturas():
        return session.query(Factura).all()
   