from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller

@api.route('/user/<int:id>/debts')
def api_GetDebtList(id):
    currentdebt = Controller.cal_debt_current(id)
    return jsonify(currentdebt)


@api.route('/user/<int:id>/adddebt',methods=['POST'])
def api_AddDebt(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    res = {
        'uid':id,
        'msg':b
        }
    return jsonify(res)
