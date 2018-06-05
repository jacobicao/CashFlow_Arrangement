from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/user/<int:id>/cards')
def api_GetCardList(id):
    cardlist = Controller.card_list(id)
    return jsonify(cardlist)


@api.route('/user/<int:id>/addcard',methods=['POST'])
def api_AddCard(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('name')
    a = b.get('acdate')
    p = b.get('padate')
    n = b.get('num')
    c = b.get('isCredit')
    if not all([s,a,p,n,c]):
        res = {'err': 1, 'msg': '参数不完整'}
        return jsonify(res)
    res = Controller.add_one_card(id,s,a,p,n,c)
    return jsonify(res)
