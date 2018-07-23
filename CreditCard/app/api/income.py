# -*- coding: UTF-8 -*-
from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/incomes',methods=['POST'])
def api_GetIncomeList():
    return jsonify(Controller.income_list(g.current_user.id))


@api.route('/incomegos',methods=['POST'])
def api_GetIncomeGoList():
    return jsonify(Controller.incomego_list(g.current_user.id))


@api.route('/addincome',methods=['POST'])
def api_AddIncome():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    n = b.get('num')
    d = b.get('date')
    if not all([n,d]):
        res = {'stutas': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_income(id,n,d)
    return jsonify(res)


@api.route('/delincome',methods=['POST'])
def api_DelIncome():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    iid = b.get('id')
    if iid is None:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_income(id,iid)
    return jsonify(res)


@api.route('/delincomego',methods=['POST'])
def api_DelIncomeGo():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    gid = b.get('id')
    if not gid:
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.delete_one_incomego(id,gid)
    return jsonify(res)
