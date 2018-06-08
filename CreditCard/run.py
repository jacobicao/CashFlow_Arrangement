#!/usr/bin/env python
# encoding: utf-8
import app.model.MyApi as MyApi
import os
from app import create_app, db
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


def inner_logic(uid):
    if uid == 0:
        return
    MyApi.general_logic(MyApi.record_word, MyApi.record_program, uid)


def outer_logic(f):
    MyApi.general_logic(MyApi.login_word, MyApi.login_program, f)


def main():
    outer_logic(inner_logic)


if __name__ == "__main__":
    main()
