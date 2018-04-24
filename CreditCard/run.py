#!/usr/bin/env python
# encoding: utf-8
import MyApi


def main():
    uid = MyApi.find_user_id('Vicky')
    dt = '2018-02-01'

    pad = MyApi.get_pad()
    MyApi.init_pad(pad,uid)
    iic = MyApi.get_ic(uid)
    MyApi.show_plan(pad,iic,dt)


if __name__ == "__main__":
    main()
