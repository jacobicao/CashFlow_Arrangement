# -*- coding: UTF-8 -*-
#!/usr/bin/env python
"""
需求列表：
1. 小额贷也纳入卡包，然后考虑贷款利息
2. 可能的话应该尽量迟还，要智能
3. 分view层
"""
import datetime as dt
from .util import datetime_offset_by_month, cal_repay_date

# permit cash out on D days after statement date
D = 10
# permit repay on C days before repayment date
C = 1
# constance
DayO = dt.timedelta(days=0)
Day4 = dt.timedelta(days=D)


class CreditCard:
    def __init__(self, sub, cid, name, d1, d2, limit, ct = 1):
        if d1 > 28:
            raise Exception('The statement date must less than 29!')
        self.statement_date = d1
        if d2 > 28:
            raise Exception('The repay date must less than 29!')
        self.repay_date = d2
        self.cid = cid
        self.name = name
        self.limit = limit
        self.debt = 0
        self.debt_list = {}
        self.load = False
        self.ct = ct  # card type
        self.sub = sub
        self.sub.attach(self)

    def __repr__(self):
        return 'Card %s: %5.2f' % (self.name, self.debt)

    def should_cash_out(self, d):
        if self.ct == 0:
            return False
        if self.debt >= self.limit * 0.8:
            return False
        d1 = d.replace(day=self.statement_date) #本月账单日
        d2 = datetime_offset_by_month(d.replace(day=self.statement_date),-1).date() #上月账单日
        bre1 = DayO < d - d1 < Day4
        bre2 = DayO < d - d2 < Day4
        return bre1 or bre2

    def days_betw_next_repay(self,d):
        next_repay_date = cal_repay_date(d, self.statement_date, self.repay_date)
        return (next_repay_date-d).days

    def is_over_date(self, d):
        dd = min(self.debt_list.keys())
        if d > dd:
            return True
        return False

    def need_help(self, d):
        if self.debt < 0.01:
            return False
        if self.is_over_date(d):
            return True
        if (min(self.debt_list.keys()) - d) <= dt.timedelta(days=C):
            return True
        return False

    def consume(self, d, m):
        # restrict the upper bound of the total consumption
        # if self.debt + m > self.limit:
        #     raise Exception('The consumption exceeds the credit card limit!')
        self.debt += m
        next_repay_date = cal_repay_date(d, self.statement_date, self.repay_date)
        if next_repay_date in self.debt_list.keys():
            self.debt_list[next_repay_date] += m
        else:
            self.debt_list[next_repay_date] = m

    def repay(self, m):
        if not len(self.debt_list):
            print('%s has no debt to be paid!'%self.name)
            return
        self.debt -= m
        dd = min(self.debt_list.keys())
        self.debt_list[dd] -= m
        if 0 == self.debt_list[dd]:
            self.debt_list.pop(dd)
            self.load = False

    def get_first_debt_date(self):
        if 0 == len(self.debt_list):
            return
        return min(self.debt_list.keys())

    def get_this_debt(self, t):
        if 0 == len(self.debt_list):
            return 0
        dd = min(self.debt_list.keys())
        if dd - t > Day4:
            return 0
        return self.debt_list[dd]

    def get_name(self):
        if self.load:
            return '网贷'
        else:
            return self.name
