from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/incomes')
def api_GetIncomeList(id):
    return jsonify(Controller.income_list(id))


@api.route('/user/<int:id>/incomegos')
def api_GetIncomeGoList(id):
    return jsonify(Controller.incomego_list(id))


@api.route('/user/<int:id>/addincome',methods=['POST'])
def api_AddIncome(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    n = b.get('num')
    d = b.get('date')
    if not all([n,d]):
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_income(id,n,d)
    return jsonify(res)


@api.route('/user/<int:id>/delincome',methods=['POST'])
def api_DelIncome(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    iid = b.get('iid')
    if not iid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_income(id,iid)
    return jsonify(res)


@api.route('/user/<int:id>/delincomego',methods=['POST'])
def api_DelIncomeGo(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    gid = b.get('gid')
    if not gid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_incomego(id,gid)
    return jsonify(res)
