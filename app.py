import os

from flask import Flask, request

from conf.code import ResponseCode
from conf.env import mysqlConf, serverConf
from conf.logConf import logger
from routes.account import account
from routes.cart import cart
from routes.goods import goods
from rules.accountRules import Account
from rules.cartRules import Cart
from rules.goodsRule import Goods
from utils.dbconn import db

app = Flask(__name__)

# 数据库连接配置
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{mysqlConf['user']}:{mysqlConf['password']}@"
    f"{mysqlConf['host']}:{mysqlConf['port']}/{mysqlConf['database']}?charset=utf8mb4"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.ensure_ascii = False

db.init_app(app)

# 接口校验规则：蓝图名 -> 视图函数名 -> 规则
rules = {
    "account": Account.ruleDict,
    "goods": Goods.ruleDict,
    "cart": Cart.ruleDict,
}


@app.errorhandler(404)
def pageNotfound(err):
    return ResponseCode.NOTFOUNDERROR, 404


@app.errorhandler(500)
def serverError(err):
    logger.error(err)
    return ResponseCode.SERVERERROR, 500


@app.before_request
def paramsHandler():
    # 统一把 get 参数或 post 报文挂到 request.req，路由里直接用
    if request.method.lower() == 'get':
        request.req = {**request.args}
    elif request.method.lower() == 'post':
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                request.req = {**request.json}
            except Exception:
                request.req = {}
        else:
            request.req = {**request.form}
    else:
        request.req = {}


# 请求拦截器：校验接口是否存在、请求方法、报文格式、必传参数
@app.before_request
def appbeforequest():
    if request.method == 'OPTIONS' or request.endpoint is None:
        return None
    if '.' not in request.endpoint:
        return None

    blueprintsName, pathName = request.endpoint.split('.', 1)

    if blueprintsName not in rules or pathName not in rules[blueprintsName]:
        return "Interface Not Found", 404

    interfaceRules = rules[blueprintsName][pathName]

    if request.method.lower() != interfaceRules["method"]:
        return ResponseCode.REQUESTMETHODERROR, 405

    # post 请求校验报文形态
    if request.method.lower() == "post":
        req_content_type = request.headers.get("Content-Type", "")
        allow_content_type = interfaceRules.get("contentType", "")
        if allow_content_type and allow_content_type not in req_content_type:
            return ResponseCode.CONTENTYPEERROR, 415

    # 校验必传参数
    if "params" in interfaceRules:
        filterparams = [item for item in interfaceRules["params"] if item in request.req]
        if len(filterparams) != len(interfaceRules["params"]):
            return ResponseCode.PARAMSERROR, 400


@app.route('/')
def index():
    return {"code": 1, "msg": "flask-ecommerce-api is running", "data": None}


# 绑定蓝图
app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(goods, url_prefix='/goods')
app.register_blueprint(cart, url_prefix='/cart')

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, **serverConf)
