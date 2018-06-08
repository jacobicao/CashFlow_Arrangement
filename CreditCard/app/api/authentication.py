# from flask_httpauth import HTTPBasicAuth
from flask_login import login_user, login_required, current_user
from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller
from .errors import unauthorized, forbidden
import requests
from app import db, login_manager
from app.model.DAO.DBTable import User


# auth = HTTPBasicAuth()

# def findcaller(func):
#     def wrapper(*args,**kwargs):
#         import sys
#         f=sys._getframe()
#         filename=f.f_back.f_code.co_filename
#         lineno=f.f_back.f_lineno
#         print('######################################')
#         print ('caller filename is ',filename)
#         print ('caller lineno is',lineno)
#         print ('the passed args is',args,kwargs)
#         print ('######################################')
#         func(*args,**kwargs)
#     return wrapper


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
    print(b)
    api_key = b.get('token')
    if api_key:
        user = User.verify_auth_token(api_key)
        if user:
            g.current_user = user
            g.token_used = True
            return user
    JS_CODE = b.get('code')
    # openid = get_openid(JS_CODE).get('openid')
    openid = JS_CODE
    if openid is None:
        return
    user = Controller.find_user_by_apikey(openid)
    if user is None:
        user = Controller.log_on_user(openid)
    g.current_user = user
    g.token_used = False
    return user


# @auth.verify_password
# def verify_password(username_or_token, password):
#     if username_or_token == 'code':
#         # JS_CODE = password
#         # url = 'https://api.weixin.qq.com/sns/jscode2session?'+\
#         #       'appid=%s'%current_app.config['WEAPPID']+\
#         #       '&secret=%s'%current_app.config['WESECRET']+\
#         #       '&js_code=%s'%JS_CODE+\
#         #       '&grant_type=authorization_code'
#         # openid = get_openid(url).get('openid')
#         # if openid is None:
#         #     return jsonify({'statue':0,'body':{'msg':'你传的是假code哦！'}})
#         openid = password
#         user = Controller.find_user_by_apikey(openid)
#         if user is None:
#             user = Controller.log_on_user(openid)
#         g.current_user = user
#         g.token_used = False
#         return True
#     if password == '':
#         g.current_user = User.verify_auth_token(username_or_token)
#         g.token_used = True
#         return g.current_user is not None
#     user = User.query.filter_by(username=username_or_token).first()
#     if not user:
#         return False
#     g.current_user = user
#     g.token_used = False
#     return user.verify_password(password)


@api.before_request
@login_required
def before_request():
    if g.current_user.is_anonymous:
        return forbidden('Unconfirmed account')
    if not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


@api.route('/tokens', methods=['POST'])
def get_token():
    print('get_token')
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'status':1,'body':{'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600}})


# @api.route('/login',methods=['POST'])
# def api_Login():
#     print('api_Login')
#     b = json.loads(str(request.get_data(), encoding = "utf-8"))
#     JS_CODE = b.get('code')
#     url = 'https://api.weixin.qq.com/sns/jscode2session?'+\
#           'appid=%s'%current_app.config['WEAPPID']+\
#           '&secret=%s'%current_app.config['WESECRET']+\
#           '&js_code=%s'%JS_CODE+\
#           '&grant_type=authorization_code'
#     r = get_openid(url)
#     api_key = r.get('openid')
#     if api_key is None:
#         return jsonify({'statue':0,'body':{'msg':'你传的是假code哦！'}})
#     user = Controller.find_user_by_apikey(api_key)
#     if user is None:
#         user = Controller.log_on_user(api_key)
#     login_user(user)
#     return get_token()
