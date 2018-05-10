import DAO.CardDao as CardDao

# 卡类
def card_list(uid):
    ll = []
    print('=' * 20)
    for v in CardDao.find_card(uid):
        if v[1] != '房贷':
            print('%2d:%6s' % (v[0], v[1]))
            ll.append(v[0])
    print('=' * 20)
    return ll
