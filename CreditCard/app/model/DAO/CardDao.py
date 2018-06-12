# -*- coding: UTF-8 -*-
from app import db
from .DBTable import Card


def add_card(u, s, a, p, f,ct):
    card = Card(uid=u, name=s, A_day=a, P_day=p, num=f,ct=ct)
    db.session.add(card)
    db.session.commit()


def delete_card(c):
    card = Card.query.get(c)
    card.on_use = 0
    db.session.commit()


def find_card(u):
    query = db.session.query(Card.id, Card.name, Card.A_day, Card.P_day, Card.num)
    re = query.filter(Card.uid == u, Card.on_use == 1, Card.ct == 1).all()
    return re


def find_load_account(u):
    query = db.session.query(Card.id, Card.name, Card.A_day, Card.P_day, Card.num)
    re = query.filter(Card.uid == u, Card.on_use == 1, Card.ct == 0).all()
    return re
