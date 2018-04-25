from DAO.DBTable import Income, Debt
from DAO.DBConnect import DBSession


def add_income(u, t, n):
    session = DBSession()
    income = Income(uid=u, P_time=t, num=n)
    session.add(income)
    session.commit()
    session.close()


def delete_income(i):
    session = DBSession()
    query = session.query(Income.iid)
    query.filter(Income.iid == i).delete()
    session.commit()
    session.close()


def find_income(u):
    session = DBSession()
    query = session.query(Income.P_time, Income.num)
    re = query.filter(Debt.uid == u).all()
    session.close()
    return re
