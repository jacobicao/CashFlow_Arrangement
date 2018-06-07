from flask import jsonify, request, current_app, url_for
from . import api
import json
import app.model.MyApi as Controller


@api.route('/login',methods=['POST'])
def api_Login(id):
    b = json.loads(str(request.get_data(), encoding = "utf-8"))
    s = b.get('code')
    

    oid = ''
    uid = Controller.log_on_user(oid)
    res = {'status':0,'data':{'uid':uid,'sc':oid}}
    return jsonify(res)
