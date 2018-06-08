from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller
import requests


def get_openid(url):
    h = {'content-type':'application/json'}
    r = requests.get(url,headers=h)
    return r.json()


@api.route('/login',methods=['POST'])
def api_Login():
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    JS_CODE = b.get('code')
    url = 'https://api.weixin.qq.com/sns/jscode2session?'+\
          'appid=%s'%current_app.config['WEAPPID']+\
          '&secret=%s'%current_app.config['WESECRET']+\
          '&js_code=%s'%JS_CODE+\
          '&grant_type=authorization_code'
    r = get_openid(url)
    api_key = r.get('openid')
    if api_key is None:
        return jsonify({'statue':0,'body':{'msg':'id不存在'}})
    uid = Controller.find_user_by_apikey(api_key)
    if uid == 0:
        uid = Controller.log_on_user(api_key)
    res = {'status':1,'body':{'uid':uid,'oid':api_key}}
    return jsonify(res)
