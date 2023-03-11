from sqlalchemy import Column, Integer, String, DateTime
from config import Base

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    description = Column(String(255), unique=True)
    create_time = Column(DateTime, unique=True)
    update_time = Column(DateTime, unique=True)
    price = Column(Integer, primary_key=True)
    photo = Column(String(500), unique=True)

    def __init__(self, id=None, description=None, create_time=None, update_time=None, price=None, photo=None):
        self.id = id
        self.description = description
        self.create_time = create_time
        self.update_time = update_time
        self.price = price
        self.photo = photo
