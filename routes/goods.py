from flask import Blueprint, request

from conf.code import ResponseCode
from conf.logConf import logger
from tables.goods import Goods
from utils.dbconn import db
from utils.tools import serialize

goods = Blueprint("goods", __name__)


@goods.route("/add", methods=["POST"])
def goodsAdd():
    req = request.req
    try:
        price = float(req["goodsprice"])
        if price <= 0:
            return ResponseCode.PARAMSERROR
        goodsItem = Goods(goodsname=req["goodsname"], goodsprice=price)
        db.session.add(goodsItem)
        db.session.commit()
        logger.info(f"{req['goodsname']} 添加商品成功")
        return {**ResponseCode.SUCCESSCODE, "msg": "添加商品成功", "data": serialize(goodsItem)}
    except ValueError:
        return ResponseCode.PARAMSERROR
    except Exception as result:
        db.session.rollback()
        logger.error(f"添加商品异常：{result}")
        return ResponseCode.SERVERERROR


@goods.route("/list", methods=["GET"])
def goodsList():
    req = request.req
    try:
        # 带 page/size 时分页，不带时返回全部
        if "page" in req and "size" in req:
            page = int(req["page"])
            size = int(req["size"])
            if page < 1 or size < 1:
                return ResponseCode.PARAMSERROR
            result = Goods.query.paginate(page=page, per_page=size, error_out=False)
            resultList = [serialize(s) for s in result.items]
            total = result.total
        else:
            resultList = [serialize(s) for s in Goods.query.all()]
            total = len(resultList)
        logger.info("获取商品列表成功")
        return {**ResponseCode.SUCCESSCODE, "data": resultList, "total": total}
    except ValueError:
        return ResponseCode.PARAMSERROR
    except Exception as result:
        logger.error(f"获取商品列表失败：{result}")
        return ResponseCode.SERVERERROR


@goods.route("/detail/<int:gid>", methods=["GET"])
def goodsDetail(gid):
    try:
        goodsItem = db.session.get(Goods, gid)
        if goodsItem:
            return {**ResponseCode.SUCCESSCODE, "data": serialize(goodsItem)}
        return ResponseCode.NOTFOUNDERROR
    except Exception as result:
        logger.error(f"获取商品详情失败：{result}")
        return ResponseCode.SERVERERROR
