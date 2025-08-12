from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from src.models import session, Base
from sqlalchemy.orm import relationship

class usuario (Base):
    __tablename__="usuario"
    id_usuario = Column(Integer,primary_key=True)
    correo=Column(String(200), unique=True)
    nombre_persona =Column(String(300), unique=True, nullable=False)
    nombre_usuario =Column(String(300), unique=True, nullable=False)
    contraseña = Column(String(15), nullable=False)
    tipo_usuario = Column(String(10),nullable=False)

    activo = Column(Boolean, default=True, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
   
    facturas_emitidas = relationship('Factura', back_populates='empleado_object',foreign_keys='Factura.id_empleado')
    facturas_recibidas = relationship('Factura', back_populates='cliente_object',foreign_keys='Factura.id_cliente')

    def __init__ (self,correo,nombre_persona,nombre_usuario,contraseña,tipo_usuario):
        self.correo = correo 
        self.nombre_persona =  nombre_persona
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.tipo_usuario = tipo_usuario

        
    def crear_usuario(usuario):
        usuario = session.add(usuario)
        session.commit()
        return usuario
    
    def traer_usuarios():
        usuarios = session.query(usuario).all()
        return usuarios
    
    def traer_usuarios_correo(correo):
        usuarios = session.query(usuario).filter(usuario.correo == correo).first()    
        return usuarios
    
    def traer_usuarios_usuario(nombre_usuario):
        usuarios=session.query(usuario).filter(usuario.nombre_usuario == nombre_usuario).first()  
        return usuarios    