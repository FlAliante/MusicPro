import requests
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from config import Base
from sqlalchemy.sql import func

headers = {
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json"
}

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

    def __init__(self, amount = None, amount_clp = None, amount_usd = None, status = None, buy_order = None, session_id = None, transaction_date = None,  accounting_date = None, card_detail = None, installments_number = None, payment_type_code = None, authorization_code=None, response_code=None, vci = None, token=None, url=None):
        self.vci = vci
        self.amount = amount
        self.amount_clp = amount_clp
        self.amount_usd = amount_usd
        self.status = status
        self.buy_order = buy_order
        self.session_id = session_id
        self.accounting_date = accounting_date
        self.transaction_date = transaction_date
        self.authorization_code = authorization_code
        self.payment_type_code = payment_type_code
        self.response_code = response_code
        self.installments_number = installments_number
        self.token = token
        self.url = url

    # Doc API TRANSBANK https://www.transbankdevelopers.cl/referencia/webpay?l=http#confirmar-una-transaccion
    def transaction_create(buy_order, session_id, amount, return_url):
        # Declaro URL
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        # Creo el JSON
        payload = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount,
            "return_url": return_url
        }
        #Envio la solicitud
        response = requests.post(url, json=payload, headers=headers)
        return response

    def transaction_status(token):
    #Obtengo el detalle de la transaccion   
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        response = requests.get(url, headers=headers)
        return response

    def transaction_commit(token):
    #Obtengo el detalle de la transaccion   
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        response = requests.put(url, headers=headers)
        return response

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



