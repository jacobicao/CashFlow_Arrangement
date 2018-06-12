# -*- coding: UTF-8 -*-
from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/records',methods=['POST'])
def api_GetRecordList():
    return jsonify(Controller.debt_list(g.current_user.id))


@api.route('/loans',methods=['POST'])
def api_GetLoanList():
    return jsonify(Controller.loan_list(g.current_user.id))


@api.route('/adddebt',methods=['POST'])
def api_AddDebt():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    d = b.get('date')
    if not all([s,n,d]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_debt(id,s,n,d)
    return jsonify(res)


@api.route('/deldebt',methods=['POST'])
def api_DelDebt():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    did = b.get('id')
    if not did:
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_debt(id,did)
    return jsonify(res)


@api.route('/addloan',methods=['POST'])
def api_AddLoan():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    ts = b.get('begin')
    tn = b.get('end')
    if not all([s,n,ts,tn]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_loan(id,s,n,ts,tn)
    return jsonify(res)


@api.route('/delloan',methods=['POST'])
def api_DelLoan():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    cid = b.get('cid')
    if not cid:
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_loan(id,cid)
    return jsonify(res)
