from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

engine = create_engine("mysql+pymysql://root:Lunanova105@localhost/facturacion02?charset=utf8mb4")

conection = engine.connect()

session = sessionmaker(bind=engine)

session = session()

Base = declarative_base()

Base.metadata.bind = engine


   


