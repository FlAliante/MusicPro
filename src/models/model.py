from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base
from sqlalchemy.sql import func


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



class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date = Column(DateTime, nullable=False,
                         server_default=func.current_timestamp())
    create_date = Column(DateTime, nullable=False,
                         server_default=func.current_timestamp(),
                         onupdate=func.current_timestamp())
    vci = Column(String(10), nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    buy_order = Column(String(20), nullable=False)
    session_id = Column(String(20), nullable=False)
    card_number = Column(String(4), nullable=False)
    accounting_date = Column(String(4), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    authorization_code = Column(String(20), nullable=False)
    payment_type_code = Column(String(10), nullable=False)
    response_code = Column(Integer, nullable=False)
    installments_number = Column(Integer, nullable=False)
    token = Column(String(100))
    url = Column(String(255))

    def __init__(self, vci, amount, status, buy_order, session_id, card_number, accounting_date, transaction_date, authorization_code, payment_type_code, response_code, installments_number, token=None, url=None):
        self.vci = vci
        self.amount = amount
        self.status = status
        self.buy_order = buy_order
        self.session_id = session_id
        self.card_number = card_number
        self.accounting_date = accounting_date
        self.transaction_date = transaction_date
        self.authorization_code = authorization_code
        self.payment_type_code = payment_type_code
        self.response_code = response_code
        self.installments_number = installments_number
        self.token = token
        self.url = url

