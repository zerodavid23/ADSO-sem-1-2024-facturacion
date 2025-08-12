from src.models import session, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone



class Factura(Base):
    __tablename__ = "factura"
    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column("id_usuario", Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    id_cliente = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    fecha = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
  

  
    empleado_object = relationship('usuario',foreign_keys=[id_empleado], back_populates='facturas_emitidas')
    cliente_object = relationship('usuario', foreign_keys=[id_cliente], back_populates='facturas_recibidas')
    detalles = relationship('DetalleFactura', back_populates='factura', cascade="all, delete-orphan")
    

   

    def __init__(self,id_empleado, id_cliente, fecha):
        self.id_empleado = id_empleado   
        self.id_cliente = id_cliente
        self.fecha = fecha
   
    @staticmethod   
    def crear_factura(factura):
        session.add(factura)
        session.commit()
        return factura
    @staticmethod 
    def traer_facturas():
        return session.query(Factura).all()
   
   
         