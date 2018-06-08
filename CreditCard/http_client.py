import requests
import json
from requests.auth import HTTPBasicAuth

url_base = 'http://127.0.0.1:5000'

def easy_login():
    h = {'content-type':'application/json'}
    url = url_base+'/api/v1/tokens'
    u = {'code':'caozhijie'}
    r = requests.post(url,headers=h,data=json.dumps(u))
    print(r.headers)
    print(r.json())

    print('='*30+'\n')

    token = r.json()['body']['token']
    url = url_base+'/api/v1/cards'
    u = {'token':token}
    r = requests.post(url,headers=h,data=json.dumps(u))
    print(r.headers)
    print(r.json())

easy_login()




def get_cards():
    h = {'content-type':'application/json'}
    url = url_base+'/api/v1/user/1/cards'
    r = requests.get(url,headers=h)
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
    url = url_base + '/api/v1/user/1/addcard'
    r = requests.post(url,
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
    url = url_base + '/api/v1/user/1/delcard'
    r = requests.post(url,
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
    url = url_base+'/api/v1/user/1/adddebt'
    r = requests.post(url,
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
    url = url_base+'/api/v1/user/1/deldebt'
    r = requests.post(url,
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
    r = requests.post(url,
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


def add_loan():
    u = {
        'cid':'111',
        'num':28888,
        'begin':'2018-6-6',
        'end':'2020-6-6'
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/addloan'
    r = requests.post(url,
        data=json.dumps(u),
        headers=h
        )
    print(r.json())

def del_loan():
    u = {
        'cid':'111',
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/delloan'
    r = requests.post(url,
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def add_income():
    u = {
        'num':28888,
        'date':'2018-6-6',
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/addincome'
    r = requests.post(url,
        data=json.dumps(u),
        headers=h
        )
    print(r.json())

def del_income():
    u = {
        'iid':'17',
        }
    h = {
        'content-type':'application/json',
        }
    url = url_base + '/api/v1/user/1/delincome'
    r = requests.post(url,
        data=json.dumps(u),
        headers=h
        )
    print(r.json())


def get_records():
    url = url_base+'/api/v1/user/1/records'
    r = requests.get(url)
    print(r.json())


def get_loans():
    url = url_base+'/api/v1/user/1/loans'
    r = requests.get(url)
    print(r.json())

def get_incomegos():
    url = url_base+'/api/v1/user/1/incomegos'
    r = requests.get(url)
    print(r.json())
