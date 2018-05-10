import DAO.IncomeDao as IncomeDAO
from Algorithm.util import is_float, is_days, is_date
import datetime as dt

# 收入类
def get_ic(uid):
    iic = dict()
    for v in IncomeDAO.find_income(uid):
        iic[v[0]] = int(v[1])
    return iic


def income_list(uid):
    print('='*20)
    ll = []
    for v in IncomeDAO.find_income(uid):
        print('{2}: {0}: {1:,.0f}'.format(*v))
        ll.append(v[2])
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
