import app.model.DAO.CardDao as CardDao
from app.model.Algorithm.util import is_float, is_days

def card_list(uid):
    ll = []
    for v in CardDao.find_card(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['acdate'] = v[2]
        cl['padate'] = v[3]
        cl['num'] = v[4]
        ll.append(cl)
    return ll

def load_account_list(uid):
    ll = []
    for v in CardDao.find_load_account(uid):
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['acdate'] = v[2]
        cl['padate'] = v[3]
        cl['num'] = v[4]
        ll.append(cl)
    return ll


def add_one_card(u,s,a,p,f,c):
    if not is_days(a) or not is_days(p):
        return {'msg':'日期错误','status':2}
    if not is_float(f):
        return {'msg':'额度错误','status':2}
    if c not in [0,1]:
        return {'msg':'卡类错误','status':2}
    try:
        CardDao.add_card(u, s, int(a), int(p), f, c)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'添加成功!','status':1}
    return res


def delete_one_card(uid,cid):
    if not str(cid).isdigit():
        return {'status':2,'msg':'id 不存在'}
    try:
        CardDao.delete_card(cid)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'status':2}
    else:
        res = {'msg':'删除成功:','status':1}
    return res
