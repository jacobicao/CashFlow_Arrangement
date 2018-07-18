# -*- coding: UTF-8 -*-
from app import db
from .DBTable import Repay, Card


def add_repay(u, c, t, n):
    repay = Repay(uid=u, cid=c, date=t, num=n)
    db.session.add(repay)
    db.session.commit()


def delete_repay(r):
    repay = Repay.query.get(r)
    db.session.delete(repay)
    db.session.commit()


def find_repay(u):
    query = db.session.query(Card.id, Card.name, Repay.date, Repay.num, Repay.id)
    re = query.filter(Card.id == Repay.cid, Repay.uid == u).order_by(Repay.date).all()
    return re

def find_card_repay(u,c):
    query = db.session.query(Repay.cid, Repay.date, Repay.num, Repay.id)
    re = query.filter(Repay.cid == c, Repay.uid == u).order_by(Repay.date).all()
    return re
