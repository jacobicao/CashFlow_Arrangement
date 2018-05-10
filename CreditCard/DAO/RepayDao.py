from DAO.DBTable import Debt, Card, Repay
from DAO.DBConnect import DBSession


def add_repay(u, c, t, n):
    session = DBSession()
    repay = Repay(uid=u, cid=c, P_time=t, num=n)
    session.add(repay)
    session.commit()
    session.close()


def delete_repay(u, r):
    session = DBSession()
    query = session.query(Repay.rid)
    query.filter(Repay.uid == u, Repay.rid == r).delete()
    session.commit()
    session.close()


def find_repay(u):
    session = DBSession()
    query = session.query(Card.cid, Card.name, Repay.P_time, Repay.num, Repay.rid)
    re = query.filter(Card.cid == Repay.cid, Repay.uid == u).order_by(Repay.P_time).all()
    session.close()
    return re
