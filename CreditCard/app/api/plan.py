from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/debts',methods=['POST'])
def api_GetDebtList(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('api_key')
    if not Controller.queding(id,s):
        return jsonify({'status':2,'data':{'msg':'该用户未注册'}})
    return jsonify(Controller.cal_debt_current(id))


@api.route('/user/<int:id>/plan',methods=['POST'])
def api_GetPlan(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('s')
    if not Controller.queding(id,s):
        return jsonify({'status':2,'data':{'msg':'该用户未注册'}})
    return jsonify(Controller.show_plan(id))
