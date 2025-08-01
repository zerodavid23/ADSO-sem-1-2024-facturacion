from src.models import session, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class Factura(Base):
    __tablename__ = "factura"
    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    fecha = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
  
  
    usuario_object = relationship('usuario', back_populates='facturas')
    detalles = relationship('DetalleFactura', back_populates='factura', cascade="all, delete-orphan")
    

   

    def __init__(self,id_usuario, fecha):
        self.id_usuario = id_usuario   
        self.fecha = fecha
   
    @staticmethod   
    def crear_factura(factura):
        session.add(factura)
        session.commit()
        return factura
    @staticmethod 
    def traer_facturas():
        return session.query(Factura).all()
   
   
         