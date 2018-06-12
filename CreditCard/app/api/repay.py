# -*- coding: UTF-8 -*-
from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/repays',methods=['POST'])
def api_GetRepayList():
    return jsonify(Controller.repay_list(g.current_user.id))


@api.route('/addrepay',methods=['POST'])
def api_AddRepay():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    d = b.get('date')
    if not all([s,n,d]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_repay(id,s,n,d)
    return jsonify(res)


@api.route('/delrepay',methods=['POST'])
def api_DelRepay():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    rid = b.get('id')
    if not rid:
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_repay(id,rid)
    return jsonify(res)
