from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/records')
def api_GetRecordList(id):
    return jsonify(Controller.debt_list(id))


@api.route('/user/<int:id>/loans')
def api_GetLoanList(id):
    return jsonify(Controller.loan_list(id))


@api.route('/user/<int:id>/adddebt',methods=['POST'])
def api_AddDebt(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    d = b.get('date')
    if not all([s,n,d]):
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_debt(id,s,n,d)
    return jsonify(res)


@api.route('/user/<int:id>/deldebt',methods=['POST'])
def api_DelDebt(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    did = b.get('did')
    if not did:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_debt(id,did)
    return jsonify(res)


@api.route('/user/<int:id>/addloan',methods=['POST'])
def api_AddLoan(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    ts = b.get('begin')
    tn = b.get('end')
    if not all([s,n,ts,tn]):
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_loan(id,s,n,ts,tn)
    return jsonify(res)


@api.route('/user/<int:id>/delloan',methods=['POST'])
def api_DelLoan(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    cid = b.get('cid')
    if not cid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_loan(id,cid)
    return jsonify(res)
