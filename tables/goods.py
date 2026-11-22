from sqlalchemy import Column, DECIMAL, Integer, String
from sqlalchemy.orm import relationship

from utils.dbconn import db


class Goods(db.Model):
    __tablename__ = 'goods'
    gid = Column('gid', Integer, primary_key=True, autoincrement=True)
    goodsname = Column('goodsname', String(100), nullable=False)
    goodsprice = Column('goodsprice', DECIMAL(10, 2), nullable=False)
    cart = relationship('Cart', back_populates='goods')
