import requests
import json

url_base = 'http://127.0.0.1:5000'

def get_data():
    h = {
        'content-type':'application/json',
        }
    r = requests.get(url+'/api/v1/user/1/cards',
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
    r = requests.post(url+'/api/v1/user/1/addcard',
        data=json.dumps(u),
        headers=h
        )
    print(r.headers)
    print(r.json())


def del_card():
    u = {
        'cid':'13',
        }
    h = {
        'content-type':'application/json',
        }
    r = requests.post(url+'/api/v1/user/1/delcard',
        data=json.dumps(u),
        headers=h
        )
    print(r.headers)
    print(r.json())


def add_debt():
    u = {
        'cid':'111',
        'num':28888,
        'date':'2018-6-6',
        }
    h = {
        'content-type':'application/json',
        }
    r = requests.post(url+'/api/v1/user/1/adddebt',
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def del_card():
    u = {
        'did':'58',
        }
    h = {
        'content-type':'application/json',
        }
    r = requests.post(url+'/api/v1/user/1/deldebt',
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def add_repay():
    u = {
        'cid':'111',
        'num':28888,
        'date':'2018-6-6',
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/addrepay'
    r = requests.post('http://127.0.0.1:5000/api/v1/user/1/addrepay',
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def del_repay():
    u = {
        'rid':'7',
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/delrepay'
    r = requests.post(url,
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def get_repay():
    url = url_base+'/api/v1/user/1/repays'
    r = requests.get(url)
    print(r.json())

del_repay()
