import datetime as dt
import app.model.DAO.DebtDao as DebtDao
from app.model.Algorithm.util import is_float, is_date, dateRange


def debt_list(uid):
    ll = {}
    for v in DebtDao.find_debt(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['date'] = v[2].strftime("%Y-%m-%d")
        cl['num'] = v[3]
        cl['id'] = v[4]
        if ll.get(v[0]) is None:
            ll[v[0]] = {'cid':v[0],'name':v[1],'records':[cl]}
        else:
            ll[v[0]]['records'].append(cl)
    return {'status':1,'body':{'records':list(ll.values())}}


def loan_list(uid):
    ll = []
    for v in DebtDao.find_load(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['date'] = v[2].date().strftime('%Y-%m-%d')
        cl['num'] = v[3]
        cl['id'] = v[4]
        ll.append(cl)
    return {'status':1,'body':{'loans':ll}}


def add_one_debt(uid,cid,num,t):
    if not str(cid).isdigit():
        return {'msg':'id不存在','status':2}
    if not is_float(num):
        return {'msg':'数量错误','status':2}
    if not is_date(t):
        return {'msg':'日期错误','status':2}
    try:
        DebtDao.add_debt(uid, cid, dt.datetime.strptime(t,'%Y-%m-%d'), num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功','status':1}
    return res


def delete_one_debt(uid,did):
    if not str(did).isdigit():
        return {'status':2,'msg':'id 不存在'}
    try:
        DebtDao.delete_debt(uid, int(did))
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'删除成功','status':1}
    return res


def add_loan(uid,cid,num,ts,en):
    if not str(cid).isdigit():
        return {'status':2,'msg':'id 不存在'}
    if not is_float(num):
        return {'status':2,'msg':'数量错误'}
    if not is_date(ts) or not is_date(en):
        return {'status':2,'msg':'日期错误'}
    d = dateRange(ts,en,freq='MS')
    try:
        DebtDao.add_bulk_debt(uid, cid, d, num)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功','status':1}
    return res


def delete_loan(uid,cid):
    if not str(cid).isdigit():
        return {'status':2,'msg':'id 不存在'}
    try:
        DebtDao.delete_card_debt(uid, int(cid))
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'删除成功','status':1}
    return res
