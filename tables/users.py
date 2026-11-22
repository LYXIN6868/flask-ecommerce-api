from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from utils.dbconn import db


class Users(db.Model):
    __tablename__ = 'users'
    uid = Column('uid', Integer, primary_key=True, autoincrement=True)
    username = Column('username', String(50), unique=True, nullable=False)
    password = Column('password', String(255), nullable=False)
    cart = relationship('Cart', back_populates='users')

    def setPassword(self, password):
        # 数据库中不保存明文密码
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
