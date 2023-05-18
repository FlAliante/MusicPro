from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    create_time = Column(DateTime)
    update_time = Column(DateTime) 
    price = Column(Integer)
    photo = Column(String(2000))
    url_nintendo = Column(String(500))

    def __init__(self, description, create_time, update_time, price, photo, url_nintendo):
        self.description = description
        self.create_time = create_time
        self.update_time = update_time
        self.price = price
        self.photo = photo
        self.url_nintendo = url_nintendo
    
    def to_json(self):
        return {
            "id": self.id,
            "description": self.description,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time),
            "price": self.price,
            "photo": self.photo,
            "url_nintendo": self.url_nintendo
        }


class AppProduct(Base):
    __tablename__ = 'app_product'

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    content = Column(String(255))
    codigo_barra = Column(String(255))
    nombre = Column(String(255))
    telefono_contacto = Column(String(255))
    nombre_proveedor = Column(String(255))
    descripcion = Column(String(255))

    def __init__(self, create_time, update_time, content, codigo_barra, nombre, telefono_contacto, nombre_proveedor, descripcion):
        self.create_time = create_time
        self.update_time = update_time
        self.content = content
        self.codigo_barra = codigo_barra
        self.nombre = nombre
        self.telefono_contacto = telefono_contacto
        self.nombre_proveedor = nombre_proveedor
        self.descripcion = descripcion

    def to_json(self):
        return {
            "id": self.id,
            "create_time": str(self.create_time),
            "update_time": str(self.update_time),
            "content": self.content,
            "codigo_barra": self.codigo_barra,
            "nombre": self.nombre,
            "telefono_contacto": self.telefono_contacto,
            "nombre_proveedor": self.nombre_proveedor,
            "descripcion": self.descripcion
        }


class User(Base):
    __tablename__ = 'app_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

