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


@api.route('/addexchange',methods=['POST'])
def api_AddExchange():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    d = b.get('date')
    o = b.get('oid')
    p = b.get('repaytype')
    if not all([s,n,d,p]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    if p == 1:
        res = Controller.quick_repay_by_card(id,s,n,d,o)
    elif p == 2:
        res = Controller.quick_repay_by_cash(id,s,n,d)
    elif p == 3:
        res = Controller.quick_repay_by_income(id,s,n,d,o)
    else:
        res = {'msg':'该类型还款方式暂未实现','status':2}
    return jsonify(res)
