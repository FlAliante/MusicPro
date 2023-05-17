from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
#from sqlalchemy.orm import relationship
#from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config import Base
from sqlalchemy.orm import relationship
import random


class TipoProducto(Base):
    __tablename__ = 'tipo_producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, nombre, categoria):
        self.nombre = nombre
        self.categoria = categoria

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            #"fecha_creacion": self.fecha_creacion,
            #"fecha_actualizacion": self.fecha_actualizacion,
        }


class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tipo_producto = Column(Integer, nullable=False)
    photo = Column(String(500), nullable=False)

    def __init__(self, nombre, precio, tipo_producto):
        self.nombre = nombre
        self.precio = precio
        self.tipo_producto = tipo_producto

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": str(self.precio),
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion,
            "tipo_producto_id": self.tipo_producto_id
        }
    
    # Genera una secuencia de letras mayúsculas al azar de longitud n
    def random_letters(n):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=n))

    # Genera un número entero al azar entre min y max
    def random_integer(min, max):
        return random.randint(min, max)
