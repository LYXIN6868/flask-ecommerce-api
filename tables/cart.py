from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from utils.dbconn import db


class Cart(db.Model):
    __tablename__ = 'cart'
    cid = Column('cid', Integer, primary_key=True, autoincrement=True)
    uid = Column('uid', Integer, ForeignKey('users.uid'), nullable=False)
    gid = Column('gid', Integer, ForeignKey('goods.gid'), nullable=False)
    count = Column('count', Integer, default=1, nullable=False)
    users = relationship('Users', back_populates='cart')
    goods = relationship('Goods', back_populates='cart')
    # 同一个用户对同一个商品只保留一条购物车记录
    __table_args__ = (UniqueConstraint('uid', 'gid', name='uq_cart_uid_gid'),)
