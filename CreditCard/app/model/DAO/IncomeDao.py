# -*- coding: UTF-8 -*-
from app import db
from sqlalchemy import func
from .DBTable import Income, Incomego


def add_income(u, t, n):
    income = Income(uid=u, date=t, num=n)
    db.session.add(income)
    db.session.commit()


def delete_income(iid):
    income = Income.query.get(iid)
    db.session.delete(income)
    db.session.commit()


def find_income(u):
    query = db.session.query(Income.id, Income.date, Income.num)
    re = query.filter(Income.uid == u).order_by(Income.date).all()
    return re


def add_incomego(u,i,t,n):
    incomego = Incomego(uid=u, iid=i, date=t, num=n)
    db.session.add(incomego)
    db.session.commit()


def delete_incomego(g):
    incomego = Incomego.query.get(g)
    db.session.delete(incomego)
    db.session.commit()


def find_incomego(u):
    query = db.session.query(Incomego.id, Incomego.iid, Incomego.date, Incomego.num)
    re = query.filter(Incomego.uid == u).order_by(Incomego.date).all()
    return re


def find_incomego_sum(u):
    query = db.session.query(Income.date, Income.id,
            (Income.num - func.coalesce(func.sum(Incomego.num),0)).label('num'))
    re = query.outerjoin(Incomego).group_by(Income.id).order_by(Income.date).all()
    return re
