from MySQLdb import TIMESTAMP
import requests
from sqlalchemy import DECIMAL, Column, Integer, String, DateTime
from datetime import datetime
from config import Base
from sqlalchemy.sql import func

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

class Venta(Base):
    __tablename__ = 'venta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date = Column(DateTime, nullable=False,
                            server_default=func.current_timestamp())
    create_date = Column(nullable=False,
                            server_default=func.current_timestamp(),
                            onupdate=func.current_timestamp())
    id_producto = Column(Integer)
    id_transaction = Column(Integer)
    amount_clp = Column(String(50))

    def __init__(self):
        self.id_producto = None
        self.id_transaction = None
        self.amount_clp = None

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    update_date = Column(DateTime, nullable=False,
                         server_default=func.current_timestamp())
    create_date = Column(DateTime, nullable=False,
                         server_default=func.current_timestamp(),
                         onupdate=func.current_timestamp())
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