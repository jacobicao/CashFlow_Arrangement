# -*- coding: UTF-8 -*-
from flask import Blueprint

api = Blueprint('api', __name__)

from . import card, debt, plan, repay, income, authentication
