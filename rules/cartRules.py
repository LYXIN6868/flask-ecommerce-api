class Cart:
    ruleDict = {
        'cartList': {
            "method": "get",
            "contentType": "",
            "params": []
        },
        'cartAdd': {
            "method": "post",
            "contentType": "application/json",
            "params": ['gid', 'count']
        },
        'cartUpdate': {
            "method": "post",
            "contentType": "application/json",
            "params": ['cid', 'count']
        },
        'cartDelete': {
            "method": "post",
            "contentType": "application/json",
            "params": ['cid']
        }
    }
