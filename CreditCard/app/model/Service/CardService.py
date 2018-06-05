import app.model.DAO.CardDao as CardDao
from app.model.Algorithm.util import is_float, is_days

# 卡类
def card_list(uid):
    ll = []
    # print('=' * 20)
    for v in CardDao.find_card(uid):
        # print('%2d:%6s a:%2d p:%2d e:%5d' % (v[0], v[1], v[2], v[3], v[4]))
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['acdate'] = v[2]
        cl['padate'] = v[3]
        cl['num'] = v[4]
        ll.append(cl)
        # ll.append(v[0])
    # print('=' * 20)
    return ll

def load_account_list(uid):
    ll = []
    # print('=' * 20)
    for v in CardDao.find_load_account(uid):
        # print('%2d:%6s' % (v[0], v[1]))
        cl = {}
        cl['cid'] = v[0]
        cl['name'] = v[1]
        cl['acdate'] = v[2]
        cl['padate'] = v[3]
        cl['num'] = v[4]
        ll.append(cl)
        # ll.append(v[0])
    # print('=' * 20)
    return ll


def add_one_card(u,s,a,p,f,c):
    if not is_days(a) or not is_days(p):
        return {'msg':'日期错误','err':1}
    if not is_float(f):
        return {'msg':'额度错误','err':1}
    if c not in [0,1]:
        return {'msg':'卡类错误','err':1}
    try:
        CardDao.add_card(u, s, int(a), int(p), f, c)
    except Exception as e:
        res = {'msg':'输入错误:' + str(e),'err':1}
    else:
        res = {'msg':'添加成功!','err':0}
    return res


def delete_one_card(uid):
    ll = card_list(uid)
    if not len(ll):
        print('没有卡片')
        return
    cid = input('哪张卡?')
    if not cid.isdigit(): #or int(cid) not in ll:
        print('输入错误')
        return
    CardDao.delete_card(cid)
    print('删除成功!')
