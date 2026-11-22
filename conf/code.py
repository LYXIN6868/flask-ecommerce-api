class ResponseCode:
    SUCCESSCODE = {"code": 1, "msg": "success", "data": None}
    ACCOUNTPWDERROR = {"code": -1, "msg": "用户名或密码错误", "data": None}
    TOKENTIMEOUTERROR = {"code": -2, "msg": "身份认证过期,重新登陆", "data": None}
    VERIFYTOKENERROR = {"code": -3, "msg": "身份认证失效，请重新登录", "data": None}
    PARAMSERROR = {"code": -4, "msg": "参数非法", "data": None}
    SERVERERROR = {"code": -5, "msg": "服务器内部错误", "data": None}
    REQUESTMETHODERROR = {"code": -6, "msg": "请求方式错误", "data": None}
    CONTENTYPEERROR = {"code": -7, "msg": "请求报文格式错误", "data": None}
    TOKENMISSERROR = {"code": -8, "msg": "身份认证丢失，请重新登录", "data": None}
    NOTFOUNDERROR = {"code": -9, "msg": "数据或接口不存在", "data": None}
    USEREXISTERROR = {"code": -10, "msg": "用户名已存在", "data": None}
