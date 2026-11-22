import datetime

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from conf.env import jwtConf


def createToken(useropt, timeout=None):
    if timeout is None:
        timeout = jwtConf['timeout']
    headers = {
        'alg': 'HS256',
        'typ': 'JWT'
    }
    token = jwt.encode(headers=headers, payload={
        **useropt,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=timeout)
    }, algorithm='HS256', key=jwtConf['key'])
    return token


def verifyToken(token):
    try:
        content = jwt.decode(token, key=jwtConf['key'], algorithms=['HS256'])
    except ExpiredSignatureError as result:
        print(result)
        return {"code": -1, "msg": "身份令牌失效", 'data': None}
    except InvalidTokenError as result:
        print(result)
        return {"code": -2, "msg": "身份令牌非法", 'data': None}
    else:
        return {'code': 1, 'msg': "身份认证通过", 'data': content}


if __name__ == '__main__':
    token = createToken({
        "uid": 1,
        "username": '张三'
    })
    print(token)
    content = verifyToken(token)
    print(content)
