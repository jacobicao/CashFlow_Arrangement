from Algorithm.CardPad import CardPad
from Algorithm.CreditCard import CreditCard
from Service.RepayService import quick_repay
import DAO.DebtDao as DebtDao
import DAO.CardDao as CardDao
import DAO.RepayDao as RepayDao
import DAO.IncomeDao as IncomeDao
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
    for v in DebtDao.find_debt(uid):
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
    col = ['date', 'take', 'num', 'repay','repaytype','oid','cid']
    plan = pd.DataFrame(pad.plan, columns=col)
    plan.date = pd.to_datetime(plan.date)
    return plan,a


# view
def print_plan(uid,plan,a):
    print('=' * 20)
    if not len(plan):
        print('=' * 20 + '\n没有数据')
        return
    format_er = '{}: {}: {:>6} - {:>6.0f} -> {:>6}|{},{},{}'
    dd = []
    for index, row in plan.iterrows():
        dd.append(format_er.format(index,row['date'].date(),row['take'],row['num'],row['repay'],
        row['repaytype'],row['oid'],row['cid']))
    dd = '\n'.join(dd)
    print(dd);print(a)
    print('=' * 20)
    save_plan(dd)
    tp = input('要快速还款吗(第一条)?(y/n)')
    if tp == 'y':
        # pid = input('哪一条计划?')
        pid = 0
        quick_repay(uid,plan.iloc[int(pid)])


def cal_debt_current(uid):
    pad = CardPad()
    init_pad(pad, uid)
    d = pad.get_total_debt_list()
    print('=' * 20)
    if d is None:
        print('=' * 20 + '没有数据')
        return
    d = '\n'.join(map(lambda x: '{}:{} 要还 {:.0f}'.format(*x),d))
    print(d)
    print('=' * 20)


def show_plan(uid):
    days = 365
    pad = CardPad()
    init_pad(pad, uid)
    plan,a = cal_plan(pad,days)
    print_plan(uid,plan,a)
