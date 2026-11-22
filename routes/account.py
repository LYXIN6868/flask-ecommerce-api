from flask import Blueprint, request

from conf.code import ResponseCode
from conf.env import jwtConf
from conf.logConf import logger
from tables.users import Users
from utils.dbconn import db
from utils.tokenTools import createToken

account = Blueprint('account', __name__)


@account.route('/login', methods=['post'])
def login():
    req = request.req
    try:
        user = Users.query.filter(Users.username == req['username']).first()
        if user and user.checkPassword(req['password']):
            userDict = {
                "username": user.username,
                'uid': user.uid
            }
            token = createToken(userDict, jwtConf['timeout'])
            logger.info(f"{userDict['username']} 登录成功")
            return {**ResponseCode.SUCCESSCODE, "msg": "登录成功", "data": {
                **userDict,
                "token": token
            }}
        logger.info(f"{req['username']} 登录失败，用户名或密码错误")
        return ResponseCode.ACCOUNTPWDERROR
    except Exception as result:
        db.session.rollback()
        logger.error(f"登录接口异常：{result}")
        return ResponseCode.SERVERERROR


@account.route('/register', methods=['post'])
def register():
    req = request.req
    try:
        if Users.query.filter(Users.username == req['username']).first():
            return ResponseCode.USEREXISTERROR
        user = Users(username=req['username'])
        user.setPassword(req['password'])
        db.session.add(user)
        db.session.commit()
        logger.info(f"{req['username']} 注册成功")
        return {**ResponseCode.SUCCESSCODE, "msg": "注册成功", "data": {
            "uid": user.uid,
            "username": user.username
        }}
    except Exception as result:
        db.session.rollback()
        logger.error(f"注册接口异常：{result}")
        return ResponseCode.SERVERERROR
