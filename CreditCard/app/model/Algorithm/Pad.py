#!/usr/bin/env python
# encoding: utf-8
import datetime as dt
from .util import find_income

class Pad:
    def __init__(self):
        self.pool = []
        self.income = []
        self.fee = 0
        self.plan = []
        self.radio = 0.006

    def __repr__(self):
        return ','.join([str(x.debt) for x in self.pool])

    def attach(self, card):
        self.pool.append(card)

    def get_card(self, cid):
        for c in self.pool:
            if not c.cid == cid:
                continue
            return c
        raise Exception('No card\'s id is %s' % cid)

    def get_first_date(self):
        ll = []
        for c in self.pool:
            n = c.get_first_debt_date()
            if n is None:
                continue
            ll.append(n)
        if ll == []:
            return
        return min(ll)

    def get_total_debt_list(self):
        s = []
        for c in self.pool:
            if c.ct == 0:
                continue
            s.extend([(k,c.cid,c.name,v) for k,v in c.debt_list.items()])
        s.sort(key=lambda x:x[0])
        return s

    def get_total_fee(self):
        return self.fee

    def get_total_debt(self):
        s = 0
        for c in self.pool:
            if c.ct == 0:
                continue
            s += c.debt
        return s

    def set_income(self, v):
        if v[2] < 0.01:
            return
        a = find_income(v[0],self.income)
        if a != len(self.income):
            self.income[a][2] += v[2]
        else:
            self.income.append(list(v))
            self.income.sort(key=lambda x:x[0])


    def consume(self, t, i):
        if not len(self.income):
            return
        ll = []
        while self.income[0][0]<=t and i>0:
            if self.income[0][2] > i:
                self.income[0][2] -= i
                ll.append((self.income[0][1],i))
                break
            else:
                ll.append((self.income[0][1],self.income[0][2]))
                i -= self.income[0][2]
                self.income = self.income[1:]
                if not len(self.income):
                    break
        return ll


    def get_income(self,t):
        a = 0
        for v in self.income:
            if v[0]<=t:
                a += v[2]
        return a
