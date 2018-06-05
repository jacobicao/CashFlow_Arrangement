import datetime as dt
import pandas as pd
import app.model.DAO.DebtDao as DebtDao
from app.model.Service.CardService import card_list, load_account_list
from app.model.Algorithm.util import is_float


def debt_list(uid):
    ll = []
    a = 0
    # print('=' * 20)
    for v in DebtDao.find_debt(uid):
        a+=v[3]
        # print('%2d:%s: %s 消费 %5d' % (v[4], v[2], v[1], v[3]))
        ll.append(v[4])
    # print('=' * 20)
    if len(ll):
        print('共: %6d'%a)
    return ll


def load_list(uid):
    ll = []
    a = 0
    print('=' * 20)
    for v in DebtDao.find_load(uid):
        a+=v[3]
        print('%2d:%s 消费 %5d 在 %s' % (v[4], v[1], v[3], v[2]))
        ll.append(v[4])
    print('=' * 20)
    if len(ll):
        print('共: %6d'%a)
    return ll


def add_one_debt(uid,cid,num,t):
    if not str(cid).isdigit():
        return {'msg':'输入错误','err':1}
    if not is_float(num):
        return {'msg':'输入错误','err':1}
    try:
        DebtDao.add_debt(uid, cid, dt.datetime.strptime(t,'%Y-%m-%d'), num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'err':1}
    else:
        res = {'msg':'添加成功','err':0}
    return res


def delete_one_debt(uid,did):
    if not str(did).isdigit():
        return {'err':1,'msg':'id 不存在'}
    try:
        DebtDao.delete_debt(uid, int(did))
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'err':1}
    else:
        res = {'msg':'删除成功:','err':0}
    return res


def add_loan(uid):
    ll = load_account_list(uid)
    if len(ll) == 0:
        print('当前没有贷款卡，请先添加卡片.')
        return
    cid = input('哪张卡?')
    if not cid.isdigit() or int(cid) not in ll:
        print('输入错误')
        return
    num = input('月供多少?')
    if not is_float(num):
        print('输入错误')
        return
    ts = input('开始时间(YYYY-MM-DD)?')
    en = input('结束时间(YYYY-MM-DD)?')
    d = pd.date_range(ts,en,freq='MS')
    try:
        DebtDao.add_bulk_debt(uid, cid, d, num)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')

def delete_load(uid):
    ll = load_account_list(uid)
    if len(ll) == 0:
        print('没有记录')
        return
    cid = input('哪一张卡?')
    if not cid.isdigit() or int(cid) not in ll:
        print('输入错误')
        return
    DebtDao.delete_card_debt(uid, int(cid))
    print('删除成功!')
