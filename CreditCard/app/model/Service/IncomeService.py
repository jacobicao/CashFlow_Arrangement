import datetime as dt
import app.model.DAO.IncomeDao as IncomeDAO
from app.model.Algorithm.util import is_float, is_days, is_date


def income_list(uid):
    ll = []
    for v in IncomeDAO.find_income(uid):
        cl = {}
        cl['iid'] = v[0]
        cl['date'] = v[1]
        cl['num'] = v[2]
        ll.append(cl)
    return ll


def add_one_income(uid,n,t):
    if not is_float(n):
        return {'msg':'id不存在','err':1}
    if not is_date(t):
        return {'msg':'输入错误','err':1}
    try:
        IncomeDAO.add_income(uid, dt.datetime.strptime(t,'%Y-%m-%d'), n)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'err':1}
    else:
        return {'msg':'添加成功','err':0}


def delete_one_income(uid,iid):
    if not str(iid).isdigit():
        return {'msg':'id不存在','err':1}
    try:
        IncomeDAO.delete_income(iid)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'err':1}
    else:
        return {'msg':'删除成功','err':0}


def incomego_list(uid):
    ll = []
    for v in IncomeDAO.find_incomego(uid):
        cl = {}
        cl['gid'] = v[0]
        cl['iid'] = v[1]
        cl['date'] = v[2]
        cl['num'] = v[3]
        ll.append(cl)
    return ll


def delete_one_incomego(uid,gid):
    if not str(gid).isdigit():
        return {'msg':'id不存在','err':1}
    try:
        IncomeDAO.delete_incomego(gid)
    except Exception as e:
        return {'msg':'输入错误:'+str(e),'err':1}
    else:
        return {'msg':'删除成功','err':0}
