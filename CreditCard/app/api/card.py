from flask import jsonify, request, current_app, url_for
from . import api
import json
import MyApi as Controller

@api.route('/user/<int:id>/cards')
def get_card_list(id):
    cardlist = Controller.card_list(id)
    return jsonify(cardlist)


@api.route('/user/<int:id>/plan')
def show_debt_plan(id):
    return jsonify(Controller.show_plan(id))




@api.route('/user/<int:id>/addcard',methods=['POST'])
def show_plan(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    user = {
        'uid':id,
        'msg':b
        }
    return jsonify(user)
