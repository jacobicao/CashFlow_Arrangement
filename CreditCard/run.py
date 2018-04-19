#!/usr/bin/env python
# encoding: utf-8
import csv
import pandas as pd
from Credit_card import Credit_card
from Card_pad import Card_pad, logger
from DBController import *

uid = find_user('Vicky')

def get_ic():
    iic = dict()
    for v in find_income(uid):
        iic[v[0]] = int(v[1])
    return iic

def init_pad(pad):
    for v in find_card(uid):
        Credit_card(pad,v[0],int(v[1]),int(v[2]),int(v[3]))
    for v in find_debt(uid):
        pad.get_card(v[0]).consume(v[1],int(v[2]))
    return

def main():
    pad = Card_pad()
    init_pad(pad)
    iic = get_ic()
    rng = pd.date_range('2018-2-1','2018-12-31')
    for t in rng:
        if t.date() in iic:
            pad.set_income(iic[t.date()])
        pad.check_repay(t)
    logger.info('\n%s: 当前信用卡负债还有 %.f'%(t.date(),pad.get_total_debt()))
    logger.info('%s: 区间总手续费达 %.f\n'%(t.date(),pad.get_total_fee()))

if __name__ == "__main__":
    main()
