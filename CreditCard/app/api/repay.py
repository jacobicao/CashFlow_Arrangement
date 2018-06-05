from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/repays')
def api_GetRepayList(id):
    repaylist = Controller.repay_list(id)
    return jsonify(repaylist)


@api.route('/user/<int:id>/addrepay',methods=['POST'])
def api_AddRepay(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('cid')
    n = b.get('num')
    d = b.get('date')
    if not all([s,n,d]):
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_repay(id,s,n,d)
    return jsonify(res)


@api.route('/user/<int:id>/delrepay',methods=['POST'])
def api_DelRepay(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    rid = b.get('rid')
    if not rid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_repay(id,rid)
    return jsonify(res)
