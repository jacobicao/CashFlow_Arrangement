import requests
import json

u = {'name':'jacob'}
h = {'content-type':'application/json'}
r = requests.get('http://127.0.0.1:5000/api/v1/user/1/plan',headers=h)
print(r.headers)
print(r.json())
