# -*- coding: UTF-8 -*-
import datetime as dt
import app.model.DAO.RepayDao as RepayDao
import app.model.DAO.DebtDao as DebtDao
import app.model.DAO.IncomeDao as IncomeDao
from app.model.Service.CardService import card_list
from app.model.Algorithm.util import is_float, is_date


def repay_list(uid):
    ll = {}
    for v in RepayDao.find_repay(uid):
        if v[1] == '房贷':
            continue
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
def quick_repay(uid,rc):
    in_cid = str(rc['cid'])
    num = rc['num']
    t = rc['date'].date()
    if rc['repaytype'] == 1:
        #卡还卡
        out_cid = str(rc['oid'])
        rl = round(num*1.006,2)
        DebtDao.add_debt(uid, out_cid, t, num)# 临时改为 num
        RepayDao.add_repay(uid, in_cid, t, num)
        return {'msg':'添加成功','status':1}
    elif rc['repaytype'] == 2:
        #工资还卡
        iid = int(rc['oid'])
        IncomeDao.add_incomego(uid, iid, t, num)
        RepayDao.add_repay(uid, in_cid, t, num)
        return {'msg':'添加成功','status':1}
    else:
        return {'msg':'该类型还款方式暂未实现','status':2}
