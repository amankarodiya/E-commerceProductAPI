from sqlalchemy import Column, Integer, String, Float
from .database import Base

class ProductInfo(Base):
    __tablename__ = 'ProductInfos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_name = Column(String)
    description = Column(String)
    buy_price = Column(Float)
    sell_price = Column(Float)
    quantity = Column(Integer)
