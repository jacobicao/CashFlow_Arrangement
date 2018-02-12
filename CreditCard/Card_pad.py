#!/usr/bin/env python
# encoding: utf-8
import os
if not os.path.exists('log'):
    os.mkdir('log')

class Card_pad():
    def __init__(self):
        self.pool = []
        self.date_list = dict()
        self.f1 = open('log/Cash_out_log.txt', 'w+')
        self.f2 = open('log/Overdate_log.txt', 'w+')

    def __del__(self):
        self.f1.close()
        self.f2.close()

    def Attach(self,card):
        self.pool.append(card)

    def __repr__(self):
        return ','.join([str(x.debt) for x in self.pool])

    def get_total_debt(self):
        s = 0
        for c in self.pool:
            s += c.debt
        return s

    def help_card(self,t,c):
        for cc in self.pool:
            if cc.name == c.name:
                continue
            if not cc.should_cash_out(t.date()):
                continue
            a = min(cc.limit-cc.debt,c.debt)
            print('%s: %s - %.f -> %s'%(t.date(),cc.name,a,c.name),file=self.f1)
            print('%s: %s - %.f -> %s'%(t.date(),cc.name,a,c.name))
            cc.consume(t,a)
            c.repay(a)
            if c.debt < 0.01:
                return True
        return False

    def check_repay(self,t):
        for c in self.pool:
            if not c.need_help(t,self.f2):
                continue
            if not self.help_card(t,c):
                continue

    def get_card(self,n):
        for c in self.pool:
            if not c.name == n:
                continue
            return c
        raise Exception('No card is named %s'%n)
