from flask import g, jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller
from .decorators import permission_required
from app.model.DAO.DBTable import Permission


@api.route('/reports',methods=['POST'])
def api_GetReportList():
    return jsonify(Controller.report_list(
        g.current_user.id,g.current_user.is_administrator()))


@api.route('/addreport',methods=['POST'])
def api_AddReport():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    a = b.get('is_advice')
    p = b.get('pageAdr')
    c = b.get('content')
    n = b.get('userName')
    if a is None:
        a = False
    if not all([p,c]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_report(id,a,p,c,n)
    return jsonify(res)


@api.route('/addanswer',methods=['POST'])
@permission_required(Permission.ADMIN)
def api_AddAnswer():
    id = g.current_user.id
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    d = b.get('id')
    a = b.get('ans')
    if not all([a,d]):
        res = {'status': 2, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.ans_one_answer(d,a)
    return jsonify(res)
