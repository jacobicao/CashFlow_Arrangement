import DAO.CardDao as CardDao
from Algorithm.util import is_float, is_days

# 卡类
def card_list(uid):
    ll = []
    # print('=' * 20)
    for v in CardDao.find_card(uid):
        # print('%2d:%6s' % (v[0], v[1]))
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        ll.append(cl)
    # print('=' * 20)
    return ll

def load_account_list(uid):
    ll = []
    print('=' * 20)
    for v in CardDao.find_load_account(uid):
        print('%2d:%6s' % (v[0], v[1]))
        ll.append(v[0])
    print('=' * 20)
    return ll


def add_one_card(u):
    s = input('卡名?')
    a = input('记账日?')
    if not is_days(a):
        print('输入错误')
        return
    p = input('还款日?')
    if not is_days(p):
        print('输入错误')
        return
    f = input('额度多少?')
    if not is_float(f):
        print('输入错误')
        return
    try:
        CardDao.add_card(u, s, int(a), int(p), f)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')


def delete_one_card(uid):
    ll = card_list(uid)
    if not len(ll):
        print('没有卡片')
        return
    cid = input('哪张卡?')
    if not cid.isdigit() or int(cid) not in ll:
        print('输入错误')
        return
    CardDao.delete_card(cid)
    print('删除成功!')
