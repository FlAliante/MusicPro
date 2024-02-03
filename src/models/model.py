import random
from MySQLdb import TIMESTAMP
import requests
from sqlalchemy import DECIMAL, Column, Integer, String, DateTime
from datetime import datetime
from config import Base
from sqlalchemy.sql import func


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
    marca = Column(String(100), nullable=False)
    precio = Column(DECIMAL(10, 2), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tipo_producto = Column(Integer, nullable=False)
    photo = Column(String(500), nullable=False)

    def __init__(self):
        self.nombre = None
        self.marca = None
        self.precio = None
        self.fecha_creacion = None
        self.fecha_actualizacion = None
        self.tipo_producto = None
        self.photo = None
        self.tipo_producto = None

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": str(self.precio),
            "fecha_creacion": self.fecha_creacion,
            "fecha_actualizacion": self.fecha_actualizacion,
            #"tipo_producto_id": self.tipo_producto_id
        }
    
    # Genera una secuencia de letras mayúsculas al azar de longitud n
    def random_letters(n):
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=n))

    # Genera un número entero al azar entre min y max
    def random_integer(min, max):
        return random.randint(min, max)

class Venta(Base):
    __tablename__ = 'venta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    create_date = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    id_producto = Column(Integer)
    id_transaction = Column(Integer)
    amount_clp = Column(String(50))

    def __init__(self):
        self.id_producto = None
        self.id_transaction = None
        self.amount_clp = None

    def to_dict(self):
        return {
            "id": self.id,
            "update_date": str(self.update_date),
            "create_date": str(self.create_date),
            "id_producto": self.id_producto,
            "id_transaction": self.id_transaction,
            "amount_clp": self.amount_clp
        }

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    create_date = Column(DateTime, nullable=False, server_default=func.current_timestamp(), onupdate=func.current_timestamp())
    vci = Column(String(10))
    amount = Column(Integer)
    amount_clp = Column(String(100))
    amount_usd = Column(String(100))
    status = Column(String(20))
    buy_order = Column(String(20))
    session_id = Column(String(20))
    card_detail = Column(String(100))
    accounting_date = Column(String(4))
    transaction_date = Column(DateTime)
    authorization_code = Column(String(20))
    payment_type_code = Column(String(10))
    response_code = Column(Integer)
    installments_number = Column(Integer)
    token = Column(String(100))
    url = Column(String(255))

    def __init__(self):
        self.vci = None
        self.amount = None
        self.amount_clp = None
        self.amount_usd = None
        self.status = None
        self.buy_order = None
        self.session_id = None
        self.accounting_date = None
        self.transaction_date = None
        self.authorization_code = None
        self.payment_type_code = None
        self.response_code = None
        self.installments_number = None
        self.token = None
        self.url = None

    def to_dict(self):
        return {
            "id": self.id,
            "update_date": str(self.update_date),
            "create_date": str(self.create_date),
            "vci": self.vci,
            "amount": self.amount,
            "amount_clp": self.amount_clp,
            "amount_usd": self.amount_usd,
            "status": self.status,
            "buy_order": self.buy_order,
            "session_id": self.session_id,
            "card_detail": self.card_detail,
            "accounting_date": self.accounting_date,
            "transaction_date": str(self.transaction_date),
            "authorization_code": self.authorization_code,
            "payment_type_code": self.payment_type_code,
            "response_code": self.response_code,
            "installments_number": self.installments_number,
            "token": self.token,
            "url": self.url
        }