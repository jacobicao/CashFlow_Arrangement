import DAO.DebtDao as DebtDao
from Service.CardService import card_list

# 账单类
def debt_list(uid):
    ll = []
    a = 0
    print('=' * 20)
    for v in DebtDao.find_debt(uid):
        if v[1] == '房贷':
            continue
        a+=v[3]
        print('%2d:%s 消费 %5d 在 %s' % (v[4], v[1], v[3], v[2]))
        ll.append(v[4])
    print('=' * 20)
    if len(ll):
        print('共: %6d'%a)
    else:
        print('没有记录')
    return ll


def delete_one_debt(uid):
    ll = debt_list(uid)
    if len(ll) == 0:
        return
    did = input('哪一条?')
    if not did.isdigit() or int(did) not in ll:
        print('输入错误!')
        return
    DebtDao.delete_debt(uid, int(did))
    print('删除成功!')


def add_one_debt(uid):
    ll = card_list(uid)
    if len(ll)==0:
        print('当前没有卡片，请先添加卡片.')
        return
    cid = input('哪张卡?')
    if not cid.isdigit() or int(cid) not in ll:
        print('输入错误')
        return
    num = input('刷了多少?')
    if not is_float(num):
        print('输入错误')
        return
    dt = input('什么时候(YYYY-MM-DD)?')
    try:
        DebtDao.add_debt(uid, cid, pd.to_datetime(dt).date(), num)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')
