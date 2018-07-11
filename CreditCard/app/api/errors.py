# -*- coding: UTF-8 -*-
from flask import jsonify
from . import api


def bad_request(message):
    response = jsonify({'status':2, 'error': 'bad request', 'msg': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'status':9, 'error': 'unauthorized', 'msg': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'status': 2, 'msg': '权限不足'})
    response.status_code = 403
    return response


@api.errorhandler(ValueError)
def validation_error(e):
    return bad_request(e.args[0])
