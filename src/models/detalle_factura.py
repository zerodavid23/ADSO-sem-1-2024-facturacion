from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.models import Base

class DetalleFactura(Base):
    __tablename__ = 'detalle_factura'
    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura'), nullable=False)
    id_producto = Column(Integer, ForeignKey('Producto.id_producto'), nullable=False)
    cantidad = Column(Float, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # Relaciones
    factura = relationship('Factura', back_populates='detalles')
    producto_object = relationship('Producto', back_populates='detalles')

    def __init__(self, id_factura, id_producto, cantidad, precio_unitario):
        self.id_factura = id_factura
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario


    @property
    def total(self):
            return float(self.cantidad) * float(self.producto_object.precio_unitario)
