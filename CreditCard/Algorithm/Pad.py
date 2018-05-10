#!/usr/bin/env python
# encoding: utf-8
import datetime as dt

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
        raise Exception('No card\'s id is %s' % n)

    def get_total_fee(self):
        return self.fee

    def get_total_debt(self):
        s = 0
        for c in self.pool:
            if c.name == "房贷":
                continue
            s += c.debt
        return s

    def set_income(self, iid, t, i):
        print(iid,t,i)
        return
        if t in self.income.keys():
            self.income[0][2] += i
        else:
            self.income.append((t,iid,i))

    def consume(self, t, i):
        self.income[0][2] -= i

    def get_income(self,t):
        return 0
