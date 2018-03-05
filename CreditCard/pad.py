#!/usr/bin/env python
# encoding: utf-8

class pad():
    def __init__(self):
        self.pool = []
        self.income = 0
        self.fee = 0

    def Attach(self,card):
        self.pool.append(card)

    def __repr__(self):
        return ','.join([str(x.debt) for x in self.pool])

    def get_card(self,n):
        for c in self.pool:
            if not c.name == n:
                continue
            return c
        raise Exception('No card is named %s'%n)

    def get_total_fee(self):
        return self.fee

    def get_total_debt(self):
        s = 0
        for c in self.pool:
            s += c.debt
        return s

    def set_income(self,i):
        self.income += i

    def consume(self,t,i):
        self.income -= i
