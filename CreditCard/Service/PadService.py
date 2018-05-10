from Algorithm.CardPad import CardPad
from Algorithm.CreditCard import CreditCard
from Service.IncomeService import get_ic
import DAO.DebtDao as DebtDao
import DAO.CardDao as CardDao
import DAO.RepayDao as RepayDao
import pandas as pd

# 卡包类
def init_pad(pad, uid):
    for v in CardDao.find_card(uid):
        CreditCard(pad, v[0], v[1], int(v[2]), int(v[3]), int(v[4]))
    for v in DebtDao.find_debt(uid):
        pad.get_card(v[0]).consume(v[2], int(v[3]))
    for v in RepayDao.find_repay(uid):
        pad.get_card(v[0]).repay(int(v[3]))
    return


def cal_plan(pad, iic, dt):
    rng = pd.date_range(dt, '2018-12-31')
    for t in rng:
        if t.date() in iic:
            pad.set_income(iic[t.date()])
        pad.check_repay(t)
    a = '\n%s: 当前信用卡负债还有 %.f' % (t.date(), pad.get_total_debt())
    a += ('\n%s: 区间总手续费达 %.f\n' % (t.date(), pad.get_total_fee()))
    col = ['date', 'take', 'num', 'repay']
    plan = pd.DataFrame(pad.plan, columns=col)
    # plan.index = pd.to_datetime(plan.date)
    # del plan['date']
    return plan,a


def print_plan(plan,a):
    format_er = '{}: {}: {:>6} - {:>6.0f} -> {:>6}'
    dd = []
    for index, row in plan.iterrows():
        dd.append(format_er.format(index,row['date'],row['take'],row['num'],row['repay']))
    dd = '\n'.join(dd)
    print(dd)
    print(a)
    print('=' * 20)
    s = input('要保存吗?(y/n)')
    if s=='y':
        save_plan(dd)


def save_plan(dd):
    import os
    if not os.path.exists('log'):
        os.mkdir('log')
    with open('log/CashOutPlan.txt','w') as f:
        f.write(dd)


def show_plan(uid):
    dt = '2018-01-01'
    pad = CardPad()
    init_pad(pad, uid)
    iic = get_ic(uid)
    plan,a = cal_plan(pad, iic, dt)
    print('=' * 20)
    if not len(plan):
        print('=' * 20 + '\n没有数据')
        return
    print_plan(plan,a)
