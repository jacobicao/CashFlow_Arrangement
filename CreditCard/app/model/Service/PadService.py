# -*- coding: UTF-8 -*-
from app.model.Algorithm.CardPad import CardPad
from app.model.Algorithm.CreditCard import CreditCard
from app.model.Algorithm.util import dateRange_by_days
import app.model.DAO.DebtDao as DebtDao
import app.model.DAO.CardDao as CardDao
import app.model.DAO.RepayDao as RepayDao
import app.model.DAO.IncomeDao as IncomeDao
import datetime as dt


def save_plan(plan):
    import os
    if not os.path.exists('log'):
        os.mkdir('log')
    with open('log/CashOutPlan.txt','w') as f:
        f.write(plan)


def init_pad(pad, uid):
    for v in CardDao.find_card(uid):
        CreditCard(pad, v[0], v[1], int(v[2]), int(v[3]), int(v[4]))
    for v in CardDao.find_load_account(uid):
        CreditCard(pad, v[0], v[1], int(v[2]), int(v[3]), int(v[4]),0)
    for v in DebtDao.find_debt(uid):
        pad.get_card(v[0]).consume(v[2], int(v[3]))
    for v in DebtDao.find_load(uid):
        pad.get_card(v[0]).consume(v[2], int(v[3]))
    for v in RepayDao.find_repay(uid):
        pad.get_card(v[0]).repay(int(v[3]))
    for v in IncomeDao.find_incomego_sum(uid):
        pad.set_income(v)
    return


def cal_plan(pad,days):
    dt_start = pad.get_first_date()
    if dt_start is None:
        return [],None
    dt_start -= dt.timedelta(days=10)
    rng = dateRange_by_days(dt_start,days)
    for t in rng:
        pad.check_repay(t)
    a = '\n%s: 当前信用卡负债还有 %.f' % (t, pad.get_total_debt())
    a += ('\n%s: 区间总手续费达 %.f\n' % (t, pad.get_total_fee()))
    return pad.plan,a


# view
def print_plan(uid,plan,a):
    if not len(plan):
        return {}
    res = []
    for row in plan:
        ll = {}
        ll['date'] = row[0].strftime('%Y-%m-%d')
        ll['name_out'] = row[1]
        ll['num'] = round(row[2],0)
        ll['fee'] = round(row[3],0)
        ll['name_in'] = row[4]
        ll['repaytype'] = row[5]
        ll['oid'] = row[6]
        ll['cid'] = row[7]
        res.append(ll)
    return res


def cal_debt_current(uid):
    ll = []
    pad = CardPad()
    init_pad(pad, uid)
    d = pad.get_total_debt_list()
    if not len(d):
        return {'status':1,'body':{'debts':ll}}
    for x in d:
        cl = {}
        cl['date'] = x[0].strftime('%Y-%m-%d')
        cl['cid'] = x[1]
        cl['name'] = x[2]
        cl['num'] = x[3]
        ll.append(cl)
    # print('\n'.join(map(lambda x: '{0}: {2} 需还款 {3:.0f}'.format(*x),d)))
    # print('=' * 20)
    # print('共%.0f元'%(sum(map(lambda x:x[3],d))))
    return {'status':1,'body':{'debts':ll}}


def show_plan(uid):
    days = 215
    pad = CardPad()
    init_pad(pad, uid)
    plan,a = cal_plan(pad,days)
    res = print_plan(uid,plan,a)
    return {'status':1,'body':{'plan':res}}
