import datetime as dt
import pandas as pd
import app.model.DAO.DebtDao as DebtDao
from app.model.Service.CardService import card_list, load_account_list
from app.model.Algorithm.util import is_float


def debt_list(uid):
    ll = []
    for v in DebtDao.find_debt(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['date'] = v[2]
        cl['num'] = v[3]
        cl['did'] = v[4]
        ll.append(cl)
    return ll


def load_list(uid):
    ll = []
    for v in DebtDao.find_load(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['date'] = v[2]
        cl['num'] = v[3]
        cl['did'] = v[4]
        ll.append(cl)
    return ll


def add_one_debt(uid,cid,num,t):
    if not str(cid).isdigit():
        return {'msg':'id不存在','err':1}
    if not is_float(num):
        return {'msg':'数量错误','err':1}
    if not is_date(t):
        return {'msg':'日期错误','err':1}
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
        res = {'msg':'删除成功','err':0}
    return res


def add_loan(uid,cid,num,ts,en):
    if not str(cid).isdigit():
        return {'err':1,'msg':'id 不存在'}
    if not is_float(num):
        return {'err':1,'msg':'数量错误'}
    if not is_date(ts) or not is_date(en):
        return {'err':1,'msg':'日期错误'}
    d = pd.date_range(ts,en,freq='MS')
    try:
        DebtDao.add_bulk_debt(uid, cid, d, num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'err':1}
    else:
        res = {'msg':'添加成功','err':0}
    return res


def delete_load(uid,cid):
    if not str(cid).isdigit():
        return {'err':1,'msg':'id 不存在'}
    try:
        DebtDao.delete_card_debt(uid, int(cid))
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'err':1}
    else:
        res = {'msg':'删除成功','err':0}
    return res
