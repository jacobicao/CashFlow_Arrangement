from DAO.DBController import *
from Service.CreditCard import CreditCard
from Service.CardPad import CardPad
import pandas as pd


# 收入类
def get_ic(uid):
    iic = dict()
    for v in find_income(uid):
        iic[v[0]] = int(v[1])
    return iic


# 用户类
def log_on_user(s):
    add_user(s)
    print('注册成功')
    return find_user(s)


def input_user_name():
    uid = find_user(input('输入用户名:'))
    while not uid:
        print('用户名不存在!')
        uid = find_user(input('输入用户名:'))
    return uid


# 卡类
def card_list(uid):
    l = []
    print('=' * 20)
    for v in find_card(uid):
        if v[1] != '房贷':
            print('%2d:%6s' % (v[0], v[1]))
            l.append(v[0])
    print('=' * 20)
    return l


# 账单类
def debt_list(uid):
    l = []
    print('=' * 20)
    for v in find_debt(uid):
        if v[1] == '房贷':
            continue
        print('%2d:%s 消费 %d 在 %s' % (v[4], v[1], v[3], v[2]))
        l.append(v[4])
    print('=' * 20)
    return l


def add_one_debt(uid):
    l = card_list(uid)
    cid = input('哪张卡?')
    if not int(cid) in l:
        print('输入错误')
        return
    dt = input('什么时候(YYYY-MM-DD)?')
    num = input('刷了多少?')
    while not is_float(num):
        print('请输入数字')
        num = input('刷了多少?')
    try:
        add_debt(uid, cid, pd.to_datetime(dt).date(), num)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')


def delete_one_debt(uid):
    l = debt_list(uid)
    did = int(input('哪一条?'))
    if did not in l:
        print('输入错误!')
        return
    delete_debt(uid, did)
    print('删除成功!')


# 卡包类
def init_pad(pad, uid):
    for v in find_card(uid):
        CreditCard(pad, v[0], v[1], int(v[2]), int(v[3]), int(v[4]))
    for v in find_debt(uid):
        pad.get_card(v[0]).consume(v[2], int(v[3]))
    return


def cal_plan(pad, iic, dt):
    rng = pd.date_range(dt, '2018-12-31')
    for t in rng:
        if t.date() in iic:
            pad.set_income(iic[t.date()])
        pad.check_repay(t)
    # logger.info('\n%s: 当前信用卡负债还有 %.f' % (t.date(), pad.get_total_debt()))
    # logger.info('%s: 区间总手续费达 %.f\n' % (t.date(), pad.get_total_fee()))
    plan = pd.DataFrame(pad.plan)
    plan.columns = ['date', 'take', 'num', 'repay']
    plan.index = pd.to_datetime(plan.date)
    del plan['date']
    return plan


def show_plan(uid):
    dt = '2018-01-01'
    pad = CardPad()
    init_pad(pad, uid)
    iic = get_ic(uid)
    plan = cal_plan(pad, iic, dt)
    plan.to_csv('log/Cash_out_plan.csv', float_format='%d')
    print('=' * 20)
    print(plan)
    print('=' * 20)


# 工具类
def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


record_program = {'1': show_plan,
                  '2': debt_list,
                  '3': add_one_debt,
                  '4': delete_one_debt}
record_word = '\n' \
              '(1)查看计划\n' \
              '(2)查看当前账单\n' \
              '(3)增加一条刷卡记录\n' \
              '(4)删除一条刷卡记录\n' \
              '(e)退出\n' \
              '请输入:'

login_word = '(1)登录\n' \
             '(2)注册\n' \
             '(e)退出it\n' \
             '请输入:'
login_program = progress = {'1': lambda f: f(input_user_name()),
                            '2': lambda f: f(log_on_user(input('请输入用户名:')))}


def general_logic(word, program, x):
    import time
    b = True
    while b:
        p = input(word)
        if p in program.keys():
            program[p](x)
        elif p is 'e':
            b = False
            print('拜拜!\n')
        else:
            print('输入不对，再来一次!')
            time.sleep(3)
