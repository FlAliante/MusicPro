from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

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

from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Producto(Base):
    __tablename__ = 'producto'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #tipo_producto_id = Column(Integer, ForeignKey('tipo_producto.id'), nullable=False)
    #tipo_producto = relationship("TipoProducto", back_populates="productos")

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
