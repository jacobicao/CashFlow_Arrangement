# -*- coding: UTF-8 -*-
from app import db
from .DBTable import User

def add_user(s):
    stu = User(username=s)
    db.session.add(stu)
    db.session.commit()
    return stu


def find_user(s):
    return User.query.filter(User.username == s).first()


def verify_token(api_key):
    return User.verify_auth_token(api_key)
