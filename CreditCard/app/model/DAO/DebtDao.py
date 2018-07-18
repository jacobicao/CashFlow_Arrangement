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

def find_card_debt(u,c):
    query = db.session.query(Debt.cid, Debt.date, Debt.num, Debt.id)
    re = query.filter(Debt.cid == c, Debt.uid == u)\
        .order_by(Debt.date)
    return re.all()

def find_load(u):
    query = db.session.query(Debt.cid, Card.name, Debt.date, Debt.num, Debt.id)
    re = query.filter(Card.id == Debt.cid, Debt.uid == u,
                        Card.ct == 0).order_by(Debt.date).all()
    return re


def add_bulk_debt(u,c,ts,n):
    mapping = [dict(uid=u, cid=c, date=i, num=n) for i in ts]
    db.session.bulk_insert_mappings(Debt,mapping)
    db.session.commit()


def delete_card_debt(u,c):
    res = db.session.query(Debt).filter(Debt.uid == u, Debt.cid == c)
    res.delete(synchronize_session=False)
    db.session.commit()


def find_debt_res(u):
    dd = db.session.query(Debt.cid,(func.coalesce(func.sum(Debt.num),0)).label('num'))\
            .filter(Debt.uid == u)\
            .group_by(Debt.cid).subquery()
    rr = db.session.query(Repay.cid,(func.coalesce(func.sum(Repay.num),0)).label('num'))\
            .filter(Repay.uid == u)\
            .group_by(Repay.cid).subquery()
    re = db.session.query(dd.c.cid,func.coalesce(dd.c.num,0)-func.coalesce(rr.c.num,0))\
            .outerjoin(rr,dd.c.cid==rr.c.cid)\
            .order_by(dd.c.cid)
    return re.all()
