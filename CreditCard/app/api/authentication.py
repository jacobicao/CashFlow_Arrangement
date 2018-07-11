# -*- coding: UTF-8 -*-
from flask_login import login_user, login_required, current_user
from flask import g, jsonify, request, current_app, url_for
from app import login_manager
from . import api
from app.model import MyApi as Controller
from app.api.errors import unauthorized, forbidden
import json
import requests


def get_openid(JS_CODE):
    url = 'https://api.weixin.qq.com/sns/jscode2session?'+\
          'appid=%s'%current_app.config['WEAPPID']+\
          '&secret=%s'%current_app.config['WESECRET']+\
          '&js_code=%s'%JS_CODE+\
          '&grant_type=authorization_code'
    h = {'content-type':'application/json'}
    r = requests.get(url,headers=h)
    return r.json()


@login_manager.request_loader
def load_user_from_request(request):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    api_key = b.get('token')
    if api_key:
        user = Controller.verify_token(api_key)
        if user:
            g.current_user = user
            g.token_used = True
            return user
    JS_CODE = b.get('code')
    openid = get_openid(JS_CODE).get('openid')
    if openid is None:
        return
    user = Controller.find_user_by_apikey(openid)
    if user is None:
        user = Controller.log_on_user(openid)
    g.current_user = user
    g.token_used = False
    return user


@api.before_request
@login_required
def before_request():
    if g.current_user.is_anonymous:
        return unauthorized('Invalid credentials')
    if not g.current_user.confirmed:
        return unauthorized('Invalid credentials')


@api.route('/tokens', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({
        'status':1,
        'body':{'token': g.current_user.generate_auth_token(
        expiration=3600),
        'expiration': 3600,
        'ip':1 if g.current_user.is_administrator() else 0}
        })
