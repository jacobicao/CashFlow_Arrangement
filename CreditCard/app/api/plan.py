# -*- coding: UTF-8 -*-
from flask import g, jsonify, request, current_app, url_for
from . import api
from .decorators import permission_required
from app.model.DAO.DBTable import Permission
import json
import app.model.MyApi as Controller


@api.route('/debts',methods=['POST'])
def api_GetDebtList():
    return jsonify(Controller.cal_debt_current(g.current_user.id))


@api.route('/plan',methods=['POST'])
@permission_required(Permission.PLAN)
def api_GetPlan():
    return jsonify(Controller.show_plan(g.current_user.id))
