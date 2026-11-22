class Goods:
    ruleDict = {
        'goodsAdd': {
            "method": "post",
            "contentType": "application/json",
            "params": ['goodsname', 'goodsprice']
        },
        'goodsList': {
            "method": "get",
            "contentType": "",
            "params": []
        },
        'goodsDetail': {
            "method": "get",
            "contentType": "",
            "params": []
        }
    }
