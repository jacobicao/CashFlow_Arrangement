from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/debts')
def api_GetDebtList(id):
    currentdebt = Controller.cal_debt_current(id)
    return jsonify(currentdebt)


@api.route('/user/<int:id>/plan')
def api_GetPlan(id):
    return jsonify(Controller.show_plan(id))
