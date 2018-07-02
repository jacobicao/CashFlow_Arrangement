# -*- coding: UTF-8 -*-
import datetime as dt
import app.model.DAO.RepayDao as RepayDao
import app.model.DAO.DebtDao as DebtDao
import app.model.DAO.IncomeDao as IncomeDao
from app.model.Service.CardService import card_list
from app.model.Algorithm.util import is_float, is_date
from app.model.Algorithm.CardPad import CardPad


def repay_list(uid):
    ll = {}
    for v in RepayDao.find_repay(uid):
        # if v[1] == '房贷':
        #     continue
        m = v[2].strftime("%m月")
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['date'] = v[2].strftime("%Y-%m-%d")
        cl['num'] = v[3]
        cl['id'] = v[4]
        if ll.get(m) is None:
            ll[m] = {'name':m,'records':[cl]}
        else:
            ll[m]['records'].append(cl)
    return {'status':1,'body':{'records':list(ll.values())}}


def add_one_repay(uid,cid,num,t):
    if not str(cid).isdigit():
        return {'msg':'id不存在','status':2}
    if not is_float(num):
        return {'msg':'数量错误','status':2}
    if not is_date(t):
        return {'msg':'日期错误','status':2}
    try:
        RepayDao.add_repay(uid, cid, dt.datetime.strptime(t,'%Y-%m-%d'), num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功','status':1}
    return res


def delete_one_repay(uid,rid):
    if not str(rid).isdigit():
        return {'msg':'id不存在','status':2}
    try:
        RepayDao.delete_repay(int(rid))
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':1}
    else:
        res = {'msg':'删除成功','status':1}
    return res


#TODO: 考虑事务
def quick_repay_by_card(uid,in_cid,num,date,out_cid):
    if not str(in_cid).isdigit():
        return {'msg':'id不存在','status':2}
    if not is_float(num):
        return {'msg':'数量错误','status':2}
    if not is_date(date):
        return {'msg':'日期错误','status':2}
    t = dt.datetime.strptime(date,'%Y-%m-%d')
    # rl = round(num*1.006,2)
    try:
        DebtDao.add_debt(uid, out_cid, t, num)# 临时改rl为 num
        RepayDao.add_repay(uid, in_cid, t, num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':1}
    else:
        res = {'msg':'添加成功','status':1}
    return res


#TODO: 考虑事务
def quick_repay_by_income(uid,in_cid,num,date,iid):
    if not str(in_cid).isdigit():
        return {'msg':'id不存在','status':2}
    if not is_float(num):
        return {'msg':'数量错误','status':2}
    if not is_date(date):
        return {'msg':'日期错误','status':2}
    t = dt.datetime.strptime(date,'%Y-%m-%d')
    try:
        IncomeDao.add_incomego(uid, iid, t, num)
        RepayDao.add_repay(uid, in_cid, t, num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':1}
    else:
        res = {'msg':'添加成功','status':1}
    return res


#TODO: 考虑事务
def quick_repay_by_cash(uid,in_cid,num,date):
    if not str(in_cid).isdigit():
        return {'msg':'id不存在','status':2}
    if not is_float(num):
        return {'msg':'数量错误','status':2}
    if not is_date(date):
        return {'msg':'日期错误','status':2}
    t = dt.datetime.strptime(date,'%Y-%m-%d')
    try:
        h = IncomeDao.find_income_before_date(uid, t)
        c = max(0,num-h)
        if c:
            IncomeDao.add_income(uid, t, c)
        pad = CardPad()
        for v in IncomeDao.find_incomego_sum(uid):
            pad.set_income(v)
        ll = pad.consume(t.date(),num)
        IncomeDao.add_bulk_incomego(uid, t, ll)
        RepayDao.add_repay(uid, in_cid, t, num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':1}
    else:
        res = {'msg':'添加成功','status':1}
    return res
