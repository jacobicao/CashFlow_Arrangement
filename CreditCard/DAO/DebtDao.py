from DAO.DBTable import Debt, Card
from DAO.DBConnect import DBSession


def add_debt(u, c, t, n):
    session = DBSession()
    debt = Debt(uid=u, cid=c, P_time=t, num=n)
    session.add(debt)
    session.commit()
    session.close()


def delete_debt(u, d):
    session = DBSession()
    query = session.query(Debt.did)
    query.filter(Debt.uid == u, Debt.did == d).delete()
    session.commit()
    session.close()


def find_debt(u):
    session = DBSession()
    query = session.query(Debt.cid, Card.name, Debt.P_time, Debt.num, Debt.did)
    re = query.filter(Card.cid == Debt.cid, Debt.uid == u).order_by(Debt.P_time).all()
    session.close()
    return re
