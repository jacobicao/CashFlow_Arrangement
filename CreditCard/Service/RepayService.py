import datetime as dt
import DAO.RepayDao as RepayDao
import DAO.DebtDao as DebtDao
import DAO.IncomeDao as IncomeDao
from Service.CardService import card_list
from Algorithm.util import is_float


def repay_list(uid):
    ll = []
    a = 0
    print('=' * 20)
    for v in RepayDao.find_repay(uid):
        if v[1] == '房贷':
            continue
        print('%2d: %s: %s 还款 %5d ' % (v[4], v[2], v[1], v[3]))
        ll.append(v[4])
    print('=' * 20)
    return ll


def add_one_repay(uid):
    ll = card_list(uid)
    if len(ll)==0:
        print('当前没有卡片，请先添加卡片.')
        return
    cid = input('哪张卡?')
    if not cid.isdigit() or int(cid) not in ll:
        print('输入错误')
        return
    num = input('还了多少?')
    if not is_float(num):
        print('输入错误')
        return
    t = input('什么时候(YYYY-MM-DD)?')
    try:
        RepayDao.add_repay(uid, cid, dt.datetime.strptime(t,'%Y-%m-%d'), num)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')


def delete_one_repay(uid):
    ll = repay_list(uid)
    if len(ll) == 0:
        print('没有记录')
        return
    rid = input('哪一条?')
    if not rid.isdigit() or int(rid) not in ll:
        print('输入错误')
        return
    RepayDao.delete_repay(uid, int(rid))
    print('删除成功!')

#TODO: 考虑事务
def quick_repay(uid,rc):
    print(rc)
    in_cid = str(rc['cid'])
    num = rc['num']
    t = rc['date'].date()
    if rc['repaytype']:
        #卡还卡
        out_cid = str(rc['oid'])
        rl = round(num/1.006,2)
        DebtDao.add_debt(uid, out_cid, t, num)
        RepayDao.add_repay(uid, in_cid, t, rl)
        print('添加成功!')
    else:
        print('该类型未实现')
        return
        #工资还卡
        iid = str(rc['oid'])
        IncomeDao.use_incomego(uid, iid, t, num)
        RepayDao.add_repay(uid, in_cid, t, num)
