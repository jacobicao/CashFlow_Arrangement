#!/usr/bin/env python
# encoding: utf-8
'''
需求列表：
1. 考虑定期收入
2. 统一打印接口
'''
import datetime as dt
import pandas as pd
import pandas.tseries.offsets as pto
# permit cash out on D days after statement date
D = 5
# permit repay on C days before repayment date
C = 3
# constance
DayO = dt.timedelta(days=0)
Day4 = dt.timedelta(days=D)

class Credit_card():
    def __init__(self,sub,name,d1,d2,limit):
        if d1 > 28:
            raise Exception('The statement date must less than 29!')
        self.statement_date = d1
        if d2>28:
            raise Exception('The repay date must less than 29!')
        self.repay_date = d2
        self.name = name
        self.limit = limit
        self.debt = 0
        self.debt_list = {}
        self.load = False
        self.sub = sub
        self.sub.Attach(self)

    def __repr__(self):
        return 'Card %s: %5.2f'%(self.name,self.debt)

    def should_cash_out(self,d):
        if self.debt > self.limit * 0.8:
            return False
        d1 = d.replace(day = self.statement_date)
        d2 = (d.replace(day = self.statement_date) - pto.DateOffset(months=1)).date()
        bre1 = DayO < d-d1 < Day4
        bre2 = DayO < d-d2 < Day4
        return bre1 or bre2

    def need_help(self,d,f):
        if self.debt < 0.01:
            return False
        dd = min(self.debt_list.keys())
        if d.date()>dd:
            if not self.load:
                #print('%s: %s - %.f -> %s'%(d.date()-dt.timedelta(days=1),'小额贷',self.debt_list[dd],self.name),file=self.f1)
                print('%s: %s - %.f -> %s'%(d.date()-dt.timedelta(days=1),'小额贷',self.debt_list[dd],self.name))
                self.load = True
            return True
        if (min(self.debt_list.keys())-d.date())<dt.timedelta(days=C):
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
        next_repay_date = self.cal_repay_date(d,self.statement_date,self.repay_date)
        if next_repay_date in self.debt_list.keys():
            self.debt_list[next_repay_date] += m
        else:
            self.debt_list[next_repay_date] = m

    def repay(self,m):
        self.debt -= m
        dd = min(self.debt_list.keys())
        self.debt_list[dd] -= m
        if 0 == self.debt_list[dd]:
            self.debt_list.pop(dd)
            self.load = False

    def get_this_debt(self,t):
        if 0 == len(self.debt_list):
            return 0
        dd = min(self.debt_list.keys())
        if dd - t > Day4:
            return 0
        return self.debt_list[dd]

    def get_name(self):
        if self.load:
            return '小额贷'
        else:
            return self.name