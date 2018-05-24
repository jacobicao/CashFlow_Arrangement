import DAO.IncomeDao as IncomeDAO
from Algorithm.util import is_float, is_days, is_date
import datetime as dt


def income_list(uid):
    print('='*20)
    ll = []
    for v in IncomeDAO.find_income(uid):
        print('{0:2d}: {1}: {2:.0f}'.format(*v))
        ll.append(v[0])
    print('='*20)
    return ll


def add_one_income(uid):
    n = input('月收入?')
    if not is_float(n):
        print('输入错误')
        return
    t = input('到账日期(YYYY-MM-DD)?')
    if not is_date(t):
        print('输入错误')
        return
    try:
        IncomeDAO.add_income(uid, dt.datetime.strptime(t,'%Y-%m-%d'), n)
    except Exception as e:
        print('输入错误:', e)
    else:
        print('添加成功!')


def delete_one_income(uid):
    ll = income_list(uid)
    if not len(ll):
        print('没有数据')
        return
    iid = input('哪条?')
    if not iid.isdigit() or int(iid) not in ll:
        print('输入错误')
        return
    IncomeDAO.delete_income(iid)
    print('删除成功!')


def incomego_list(uid):
    print('='*20)
    ll = []
    for v in IncomeDAO.find_incomego(uid):
        print('{0:2d}: {2}: {1}: {2:.0f}'.format(*v))
        ll.append(v[0])
    print('='*20)
    return ll


def delete_one_incomego(uid):
    ll = incomego_list(uid)
    if not len(ll):
        print('没有数据')
        return
    iid = input('哪条?')
    if not iid.isdigit() or int(iid) not in ll:
        print('输入错误')
        return
    IncomeDAO.delete_incomego(iid)
    print('删除成功!')
