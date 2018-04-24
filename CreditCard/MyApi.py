from DBController import *
from Credit_card import Credit_card
from Card_pad import Card_pad, logger
import pandas as pd


def find_user_id(s):
	return find_user(s)


def get_ic(uid):
    iic = dict()
    for v in find_income(uid):
        iic[v[0]] = int(v[1])
    return iic


def init_pad(pad,uid):
    for v in find_card(uid):
        Credit_card(pad,v[0],v[1],int(v[2]),int(v[3]),int(v[4]))
    for v in find_debt(uid):
        pad.get_card(v[0]).consume(v[2],int(v[3]))
    return


def get_pad():
    return Card_pad()


def show_plan(pad,iic,dt):
    rng = pd.date_range(dt,'2018-12-31')
    for t in rng:
        if t.date() in iic:
            pad.set_income(iic[t.date()])
        pad.check_repay(t)
    logger.info('\n%s: 当前信用卡负债还有 %.f'%(t.date(),pad.get_total_debt()))
    logger.info('%s: 区间总手续费达 %.f\n'%(t.date(),pad.get_total_fee()))
