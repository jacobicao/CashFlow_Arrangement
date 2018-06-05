from .DBTable import Card
from .DBConnect import DBSession


def add_card(u, s, a, p, f,ct):
    session = DBSession()
    card = Card(uid=u, name=s, A_day=a, P_day=p, num=f,ct=ct)
    session.add(card)
    session.commit()
    session.close()


def delete_card(c):
    session = DBSession()
    query = session.query(Card.cid,Card.on_use)
    s = query.filter(Card.cid == c).update({Card.on_use:0})
    session.commit()
    session.close()


def find_card(u):
    session = DBSession()
    query = session.query(Card.cid, Card.name, Card.A_day, Card.P_day, Card.num)
    re = query.filter(Card.uid == u, Card.on_use == 1, Card.ct == 1).all()
    session.close()
    return re


def find_load_account(u):
    session = DBSession()
    query = session.query(Card.cid, Card.name, Card.A_day, Card.P_day, Card.num)
    re = query.filter(Card.uid == u, Card.on_use == 1, Card.ct == 0).all()
    session.close()
    return re
