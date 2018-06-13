# -*- coding: UTF-8 -*-
from app import db
from .DBTable import Debt, Card, Repay
from sqlalchemy import func

def add_debt(u, c, t, n):
    debt = Debt(uid=u, cid=c, date=t, num=n)
    db.session.add(debt)
    db.session.commit()


def delete_debt(u, d):
    debt = Debt.query.get(d)
    db.session.delete(debt)
    db.session.commit()


def find_debt(u):
    query = db.session.query(Debt.cid, Card.name, Debt.date, Debt.num, Debt.id)
    re = query.filter(Card.id == Debt.cid, Debt.uid == u,
                        Card.ct == 1).order_by(Debt.date).all()
    return re


def find_load(u):
    query = db.session.query(Debt.cid, Card.name, Debt.date, Debt.num, Debt.id)
    re = query.filter(Card.id == Debt.cid, Debt.uid == u,
                        Card.ct == 0).order_by(Debt.date).all()
    return re


def add_bulk_debt(u,c,ts,n):
    mapping = [dict(uid=u, cid=c, date=i, num=n) for i in ts]
    db.session.bulk_insert_mappings(Debt,mapping)
    db.ession.commit()


def delete_card_debt(u,c):
    debts = Debt.query.filter(Debt.uid == u, Debt.cid == c)
    db.session.delete(debts)
    db.session.commit()


def find_debt_res(u):
    query = db.session.query(Debt.cid,
            (func.coalesce(func.sum(Debt.num),0) -
            func.coalesce(func.sum(Repay.num),0)).label('num'))
    re = query.outerjoin(Repay, Repay.cid == Debt.cid).filter(Debt.uid == u).group_by(Repay.cid)
    # query = db.session.query(Debt.cid,func.coalesce(func.sum(Debt.num),0).label('num'))
    # re = query.filter(Debt.uid == u).group_by(Debt.cid).all()
    return re.all()
