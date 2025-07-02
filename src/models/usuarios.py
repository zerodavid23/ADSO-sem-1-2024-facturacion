from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.models import session, Base


class usuario (Base):
    __tablename__="usuario"
    id_usuario = Column(Integer,primary_key=True)
    correo=Column(String(200), unique=True)
    nombre_persona =Column(String(300), unique=True, nullable=False)
    nombre_usuario =Column(String(300), unique=True, nullable=False)
    contraseña = Column(String(15), nullable=False)
    categoria =Column (Integer,ForeignKey('Categoria.id'), nullable=False)
   


    def __init__ (self,correo,nombre_persona,nombre_usuario,contraseña,categoria):
        self.correo = correo 
        self.nombre_persona =  nombre_persona
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.categoria = categoria

        
    def crear_usuario(usuario):
        usuario = session.add(usuario)
        session.commit()
        return usuario
    
    def traer_usuarios():
        usuarios = session.query(usuario).all()
        return usuarios
    