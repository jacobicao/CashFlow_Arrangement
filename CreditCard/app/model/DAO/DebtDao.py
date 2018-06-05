from .DBTable import Debt, Card
from .DBConnect import DBSession


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
    re = query.filter(Card.cid == Debt.cid, Debt.uid == u,
                        Card.ct == 1).order_by(Debt.P_time).all()
    session.close()
    return re


def find_load(u):
    session = DBSession()
    query = session.query(Debt.cid, Card.name, Debt.P_time, Debt.num, Debt.did)
    re = query.filter(Card.cid == Debt.cid, Debt.uid == u,
                        Card.ct == 0).order_by(Debt.P_time).all()
    session.close()
    return re


def add_bulk_debt(u,c,ts,n):
    session = DBSession()
    mapping = [dict(uid=u, cid=c, P_time=i, num=n) for i in ts]
    session.bulk_insert_mappings(Debt,mapping)
    session.commit()
    session.close()


def delete_card_debt(u,c):
    session = DBSession()
    query = session.query(Debt.uid,Debt.cid)
    query.filter(Debt.uid == u, Debt.cid == c).delete()
    session.commit()
    session.close()
