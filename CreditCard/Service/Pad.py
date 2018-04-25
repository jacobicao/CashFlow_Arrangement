#!/usr/bin/env python
# encoding: utf-8


class Pad:
    def __init__(self):
        self.pool = []
        self.income = 0
        self.fee = 0
        self.plan = []

    def __repr__(self):
        return ','.join([str(x.debt) for x in self.pool])

    def attach(self, card):
        self.pool.append(card)

    def get_card(self, n):
        for c in self.pool:
            if not c.id == n:
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

    def set_income(self, i):
        self.income += i

    def consume(self, t, i):
        self.income -= i
