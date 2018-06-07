from app.model.Algorithm.CardPad import CardPad, pdcol
from app.model.Algorithm.CreditCard import CreditCard
from app.model.Service.RepayService import quick_repay
import app.model.DAO.DebtDao as DebtDao
import app.model.DAO.CardDao as CardDao
import app.model.DAO.RepayDao as RepayDao
import app.model.DAO.IncomeDao as IncomeDao
import pandas as pd
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
    dt_start -= dt.timedelta(days=1)
    rng = pd.date_range(dt_start,periods=days).date
    for t in rng:
        pad.check_repay(t)
    a = '\n%s: 当前信用卡负债还有 %.f' % (t, pad.get_total_debt())
    a += ('\n%s: 区间总手续费达 %.f\n' % (t, pad.get_total_fee()))
    plan = pd.DataFrame(pad.plan, columns=pdcol)
    plan.date = pd.to_datetime(plan.date)
    return plan,a


# view
def print_plan(uid,plan,a):
    if not len(plan):
        return {}
    format_er = '{}: {:4s} -> {:6.0f} + {:3.0f} -> {:4s}'
    dd = []
    res = []
    for index, row in plan.iterrows():
        dd.append(format_er.format(row['date'].date(),row['take'],row['num'],row['fee'],row['repay']))
        ll = {}
        ll['date'] = row['date'].date().strftime('%Y-%m-%d')
        ll['name_out'] = row['take']
        ll['num'] = round(row['num'],0)
        ll['fee'] = round(row['fee'],0)
        ll['name_in'] = row['repay']
        res.append(ll)
    dd = '\n'.join(dd)
    print(dd);print(a)
    print('=' * 20)
    # save_plan(dd)
    # tp = input('已执行第一条?(y/n)')
    # if tp == 'y':
    #     # pid = input('哪一条计划?')
    #     pid = 0
    #     quick_repay(uid,plan.iloc[int(pid)])
    return res


def cal_debt_current(uid):
    pad = CardPad()
    init_pad(pad, uid)
    d = pad.get_total_debt_list()
    if d is None:
        return {}
    ll = []
    for x in d:
        cl = {}
        cl['date'] = x[0].strftime('%Y-%m-%d')
        cl['cid'] = x[1]
        cl['name'] = x[2]
        cl['num'] = x[3]
        ll.append(cl)
    print('\n'.join(map(lambda x: '{0}: {2} 需还款 {3:.0f}'.format(*x),d)))
    print('=' * 20)
    print('共%.0f元'%(sum(map(lambda x:x[3],d))))
    return {'status':1,'body':{'debts':ll}}


def show_plan(uid):
    days = 215
    pad = CardPad()
    init_pad(pad, uid)
    plan,a = cal_plan(pad,days)
    res = print_plan(uid,plan,a)
    return {'status':1,'body':{'plan':res}}
