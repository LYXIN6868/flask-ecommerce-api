class Account:
    ruleDict = {
        'login': {
            "method": "post",
            "contentType": "application/json",
            "params": ['username', 'password']
        },
        'register': {
            "method": "post",
            "contentType": "application/json",
            "params": ['username', 'password']
        }
    }
