from Service.CardPad import CardPad
from Service.CreditCard import CreditCard
from Service.IncomeApi import get_ic
import DAO.DebtDao as DebtDao
import DAO.CardDao as CardDao

# 卡包类
def init_pad(pad, uid):
    for v in CardDao.find_card(uid):
        CreditCard(pad, v[0], v[1], int(v[2]), int(v[3]), int(v[4]))
    for v in DebtDao.find_debt(uid):
        pad.get_card(v[0]).consume(v[2], int(v[3]))
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
    plan.index = pd.to_datetime(plan.date)
    del plan['date']
    return plan,a


def show_plan(uid):
    dt = '2018-01-01'
    pad = CardPad()
    init_pad(pad, uid)
    iic = get_ic(uid)
    plan,a = cal_plan(pad, iic, dt)
    print('=' * 20)
    if len(plan) == 0:
        print('=' * 20)
        print('没有数据')
        return
    print(plan)
    print(a)
    print('=' * 20)
    s = input('要保存吗?(y/n)')
    if s=='y':
        import os
        if not os.path.exists('log'):
            os.mkdir('log')
        plan.to_csv('log/Cash_out_plan.csv', float_format='%d')
