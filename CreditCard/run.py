#!/usr/bin/env python
# encoding: utf-8
import MyApi


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
