import requests
import json


def get_data():
    h = {
        'content-type':'application/json',
        }
    r = requests.get('http://127.0.0.1:5000/api/v1/user/1/cards',
        headers=h
        )
    print(r.headers)
    print(r.json())


def add_card():
    u = {
        'name':'test_card',
        'acdate':'5',
        'padate':17,
        'num':28888,
        'isCredit':1,
        }
    h = {
        'content-type':'application/json',
        }
    r = requests.post('http://127.0.0.1:5000/api/v1/user/1/addcard',
        data=json.dumps(u),
        headers=h
        )
    print(r.headers)
    print(r.json())


get_data()
