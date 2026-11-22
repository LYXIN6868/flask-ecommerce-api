from app import app
from tables.goods import Goods
from tables.users import Users
from utils.dbconn import db


def seed():
    with app.app_context():
        # 按模型建表，重复执行不会报错
        db.create_all()

        if not Users.query.filter(Users.username == 'admin').first():
            user = Users(username='admin')
            user.setPassword('123456')
            db.session.add(user)
            print('创建演示用户：admin / 123456')

        if Goods.query.count() == 0:
            goodsList = [
                Goods(goodsname='皮夹克', goodsprice=299.00),
                Goods(goodsname='皮带', goodsprice=89.00),
                Goods(goodsname='皮鞋', goodsprice=399.00),
                Goods(goodsname='连衣裙', goodsprice=199.00),
                Goods(goodsname='高跟鞋', goodsprice=259.00),
                Goods(goodsname='帆布鞋', goodsprice=159.00),
            ]
            db.session.add_all(goodsList)
            print(f'写入 {len(goodsList)} 条商品数据')

        db.session.commit()
        print('数据初始化完成')


if __name__ == '__main__':
    seed()
