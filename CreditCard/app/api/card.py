# -*- coding: UTF-8 -*-
from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/cards',methods=['POST'])
def api_GetCardList():
    return jsonify(Controller.card_list(g.current_user.id))


@api.route('/addcard',methods=['POST'])
def api_AddCard():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('name')
    a = b.get('acdate')
    p = b.get('padate')
    n = b.get('num')
    c = b.get('isCredit')
    if not all([s,a,p,n,c]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_card(id,s,a,p,n,c)
    return jsonify(res)


@api.route('/delcard',methods=['POST'])
def api_DelCard():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    cid = b.get('id')
    if not cid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_card(id,cid)
    return jsonify(res)
