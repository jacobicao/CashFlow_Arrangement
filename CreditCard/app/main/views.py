# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
import datetime

@main.route('/')
def index():
    s = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return '<h1>Hello, you just login at %s</h1>.'%s
