#!/usr/bin/env python
# encoding: utf-8
import datetime as dt
import pandas as pd
import pandas.tseries.offsets as pto
# permit cash out on D days after statement date
D = 10
# permit repay on C days before repayment date
C = 3
import os
if not os.path.exists('log'):
    os.mkdir('log')
f1 = open('log/Cash_out_log.txt', 'w+')
f2 = open('log/Overdate_log.txt', 'w+')

class Credit_card():
    def __init__(self,sub,name,d1,d2,limit,debt):
        self.name = name
        if d1 > 28:
            raise Exception('The statement date must less than 29!')
        self.statement_date = d1
        if d2>28:
            raise Exception('The repay date must less than 29!')
        self.repay_date = d2
        self.limit = limit
        self.debt = debt
        self.next_repay_date = dt.date(2010,1,1)
        self.delay_num = 0
        self.sub = sub
        self.sub.Attach(self)

    def __repr__(self):
        return 'Card %s: %5.2f'%(self.name,self.debt)

    def should_cash_out(self,d):
        if self.debt > self.limit * 0.8:
            return False
        DayO = dt.timedelta(days=0)
        Day4 = dt.timedelta(days=D)
        d1 = d.replace(day = self.statement_date)
        d2 = (d.replace(day = self.statement_date) - pto.DateOffset(months=1)).date()
        bre1 = DayO < d-d1 < Day4
        bre2 = DayO < d-d2 < Day4
        return bre1 or bre2

    def need_help(self,d):
        if self.debt < 0.01:
            return False
        if d.date()>self.next_repay_date:
            print('%s: %s有 %.f 逾期啦!'%(d.date(),self.name,self.debt),file=f2)
            print('%s: %s有 %.f 逾期啦!'%(d.date(),self.name,self.debt))
        if (self.next_repay_date-d.date())<dt.timedelta(days=C):
            return True
        return False

    def cal_repay_date(self,d,state,repay):
        this_month_statement_date = d.replace(day=state)
        if d <= this_month_statement_date and state < repay:
            q=0
        elif d > this_month_statement_date and state > repay:
            q=2
        else:
            q=1
        return (d.replace(day=repay)+pto.DateOffset(months=q)).date()

    def consume(self,d,m):
        if self.debt+m > self.limit:
            print('The comsume number exceeds the credit card limit!')
            return
        self.debt += m
        self.next_repay_date = self.cal_repay_date(d,self.statement_date,self.repay_date)

    def repay(self,m):
        self.debt -= m


class Card_pad():
    def __init__(self):
        self.pool = []
        self.date_list = dict()

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
            print('%s: %s - %.f -> %s'%(t.date(),cc.name,a,c.name),file=f1)
            print('%s: %s - %.f -> %s'%(t.date(),cc.name,a,c.name))
            cc.consume(t,a)
            c.repay(a)
            if c.debt < 0.01:
                return True
        return False

if __name__ == "__main__":
    pad = Card_pad()
    c1 = Credit_card(pad,'中行J',3,23,15000,0)
    c2 = Credit_card(pad,'平安J',5,23,28000,0)
    c3 = Credit_card(pad,'农行J',7,1,50000,0)
    c4 = Credit_card(pad,'招商Q',14,2,22000,0)
    c5 = Credit_card(pad,'中信J',16,4,50000,0)
    c6 = Credit_card(pad,'建设J',17,6,30000,0)
    c7 = Credit_card(pad,'平安Q',17,4,38000,0)
    c8 = Credit_card(pad,'兴业J',18,7,18000,0)
    c9 = Credit_card(pad,'浦发J',22,11,11000,0)
    c10 = Credit_card(pad,'建设Q',24,10,45000,0)
    c11 = Credit_card(pad,'中行Q',27,16,30000,0)
    rng = pd.date_range('2018-2-1','2018-12-31')
    c1.consume(pd.datetime(2018,1,20),13000)

    for t in rng:
        for c in pad.pool:
            if not c.need_help(t):
                continue
            if not pad.help_card(t,c):
                continue
    print('\n%s: 当前总负债还有 %.f'%(t.date(),pad.get_total_debt()))
