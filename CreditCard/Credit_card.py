#!/usr/bin/env python
# encoding: utf-8
'''
需求列表：
1. 不许逾期，如果确会逾期几天，立刻用小额贷过桥
2. 要允许多期账单
'''
import datetime as dt
import pandas as pd
import pandas.tseries.offsets as pto
# permit cash out on D days after statement date
D = 5
# permit repay on C days before repayment date
C = 3

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

    def need_help(self,d,f):
        if self.debt < 0.01:
            return False
        if d.date()>self.next_repay_date:
            print('%s: %s有 %.f 逾期啦!'%(d.date(),self.name,self.debt),file=f)
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
