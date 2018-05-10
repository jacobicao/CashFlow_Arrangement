from DAO.DBTable import Income, Incomego, Debt
from DAO.DBConnect import DBSession
from sqlalchemy import func

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
    query = session.query(Income.iid, Income.P_time, Income.num)
    re = query.filter(Income.uid == u).all()
    session.close()
    return re


def add_incomego(u,i,t,n):
    session = DBSession()
    incomego = Incomego(uid=u, iid=i, P_time=t, num=n)
    session.add(incomego)
    session.commit()
    session.close()


def delete_incomego(g):
    session = DBSession()
    query = session.query(Incomego.gid)
    query.filter(Incomego.gid == g).delete()
    session.commit()
    session.close()

def find_incomego(u):
    session = DBSession()
    query = session.query(Incomego.gid, Incomego.iid, Incomego.P_time, Incomego.num)
    re = query.filter(Incomego.uid == u).all()
    session.close()
    return re

def find_incomego_sum(u):
    session = DBSession()
    # query = session.query(Incomego.iid, (Income.num-func.sum(Incomego.num)).label("num")).group_by(Incomego.iid)
    query = session.query(Incomego.iid, Income.num, Incomego.num)
    re = query.filter(Income.iid == Incomego.iid).all()
    session.close()
    return re
