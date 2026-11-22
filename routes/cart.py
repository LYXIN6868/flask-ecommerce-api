from flask import Blueprint, request
from sqlalchemy import and_

from conf.code import ResponseCode
from conf.logConf import logger
from tables.cart import Cart
from tables.goods import Goods
from utils.dbconn import db
from utils.tokenTools import verifyToken

cart = Blueprint('cart', __name__)


# 购物车模块统一校验 token
@cart.before_request
def cartBeforeRequest():
    token = request.headers.get('token')
    if not token:
        return ResponseCode.TOKENMISSERROR
    result = verifyToken(token)
    if result['code'] == 1:
        request.uid = result['data']['uid']
    elif result['code'] == -1:
        return ResponseCode.TOKENTIMEOUTERROR
    else:
        return ResponseCode.VERIFYTOKENERROR


@cart.route('/list', methods=['get'])
def cartList():
    req = request.req
    try:
        # 购物车表和商品表联查，返回商品名称和单价
        query = db.session.query(
            Cart.cid, Goods.goodsname, Goods.goodsprice, Goods.gid, Cart.count
        ).select_from(Cart).join(Goods, Cart.gid == Goods.gid).filter(Cart.uid == request.uid)

        if 'page' in req and 'size' in req:
            page = int(req['page'])
            size = int(req['size'])
            if page < 1 or size < 1:
                return ResponseCode.PARAMSERROR
            result = query.paginate(page=page, per_page=size, error_out=False)
            rows = result.items
            total = result.total
        else:
            rows = query.all()
            total = len(rows)

        resultList = []
        for s in rows:
            resultList.append({
                "cid": s[0],
                "goodsName": s[1],
                "goodsPrice": float(s[2]),
                "goodsID": s[3],
                "count": s[4]
            })
        return {**ResponseCode.SUCCESSCODE, 'data': resultList, 'total': total}
    except ValueError:
        return ResponseCode.PARAMSERROR
    except Exception as result:
        logger.error(f'获取购物车列表失败：{result}')
        return ResponseCode.SERVERERROR


@cart.route('/add', methods=['post'])
def cartAdd():
    req = request.req
    try:
        count = int(req['count'])
        if count <= 0:
            return ResponseCode.PARAMSERROR
        goodsItem = db.session.get(Goods, req['gid'])
        if not goodsItem:
            return ResponseCode.PARAMSERROR

        # 该用户购物车里已有这个商品就累加数量，没有就新增
        cartItem = Cart.query.filter(and_(Cart.uid == request.uid, Cart.gid == req['gid'])).first()
        if cartItem:
            cartItem.count += count
        else:
            cartItem = Cart(uid=request.uid, gid=req['gid'], count=count)
            db.session.add(cartItem)
        db.session.commit()
        logger.info(f"用户 {request.uid} 添加商品 {req['gid']} 到购物车")
        return {**ResponseCode.SUCCESSCODE, 'msg': '加入购物车成功', 'data': {
            'cid': cartItem.cid,
            'gid': cartItem.gid,
            'count': cartItem.count
        }}
    except ValueError:
        return ResponseCode.PARAMSERROR
    except Exception as result:
        db.session.rollback()
        logger.error(f'添加购物车失败：{result}')
        return ResponseCode.SERVERERROR


@cart.route('/update', methods=['post'])
def cartUpdate():
    req = request.req
    try:
        count = int(req['count'])
        if count <= 0:
            return ResponseCode.PARAMSERROR
        cartItem = Cart.query.filter(and_(Cart.cid == req['cid'], Cart.uid == request.uid)).first()
        if not cartItem:
            return ResponseCode.PARAMSERROR
        cartItem.count = count
        db.session.commit()
        logger.info(f"用户 {request.uid} 修改购物车 {req['cid']} 数量为 {count}")
        return {**ResponseCode.SUCCESSCODE, 'msg': '修改成功', 'data': {
            'cid': cartItem.cid,
            'count': cartItem.count
        }}
    except ValueError:
        return ResponseCode.PARAMSERROR
    except Exception as result:
        db.session.rollback()
        logger.error(f'修改购物车失败：{result}')
        return ResponseCode.SERVERERROR


@cart.route('/delete', methods=['post'])
def cartDelete():
    req = request.req
    try:
        # 只能删除自己购物车里的数据
        cartItem = Cart.query.filter(and_(Cart.cid == req['cid'], Cart.uid == request.uid)).first()
        if not cartItem:
            return ResponseCode.PARAMSERROR
        db.session.delete(cartItem)
        db.session.commit()
        logger.info(f"用户 {request.uid} 删除购物车 {req['cid']}")
        return {**ResponseCode.SUCCESSCODE, 'msg': '删除成功', 'data': {'cid': req['cid']}}
    except Exception as result:
        db.session.rollback()
        logger.error(f'删除购物车失败：{result}')
        return ResponseCode.SERVERERROR
