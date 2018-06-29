# -*- coding: UTF-8 -*-
import datetime as dt
import app.model.DAO.IncomeDao as IncomeDAO
from app.model.Algorithm.util import is_float, is_days, is_date


def income_list(uid):
    ll = {}
    for v in IncomeDAO.find_income(uid):
        cl = {}
        cl['id'] = v[0]
        cl['date'] = v[1].strftime("%Y-%m-%d")
        cl['num'] = v[2]
        cl['typename'] = '到账'
        cl['type'] = 1
        m = v[1].strftime("%m月")
        if ll.get(m) is None:
            ll[m] = {'month':m,'records':[cl]}
        else:
            ll[m]['records'].append(cl)
    for v in IncomeDAO.find_incomego(uid):
        cl = {}
        cl['id'] = v[0]
        cl['date'] = v[2].strftime("%Y-%m-%d")
        cl['num'] = v[3]
        cl['typename'] = '支出'
        cl['type'] = 0
        m = v[2].strftime("%m月")
        if ll.get(m) is None:
            ll[m] = {'month':m,'records':[cl]}
        else:
            ll[m]['records'].append(cl)
    ll = list(ll.values())
    for v in ll:
        v['records'] = sorted(v['records'],key=lambda x: x['date'])
    return {'status':1,'body':{'records':ll}}


def add_one_income(uid,n,t):
    if not is_float(n):
        return {'msg':'id不存在','status':2}
    if not is_date(t):
        return {'msg':'输入错误','status':2}
    try:
        IncomeDAO.add_income(uid, dt.datetime.strptime(t,'%Y-%m-%d'), n)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'status':2}
    else:
        return {'msg':'添加成功','status':1}


def delete_one_income(uid,iid):
    if not str(iid).isdigit():
        return {'msg':'id不存在','status':2}
    try:
        IncomeDAO.delete_income(iid)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'status':2}
    else:
        return {'msg':'删除成功','status':1}


def delete_one_incomego(uid,gid):
    if not str(gid).isdigit():
        return {'msg':'id不存在','status':2}
    try:
        IncomeDAO.delete_incomego(gid)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'status':2}
    else:
        return {'msg':'删除成功','status':1}
