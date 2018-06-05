#!/usr/bin/env python
# encoding: utf-8
from .Pad import Pad
import datetime as dt

Day1 = dt.timedelta(days=1)
pdcol = ['date', 'take', 'num', 'fee', 'repay','repaytype','oid','cid']

class CardPad(Pad):
    def transform_debt(self, t, cc, cn, num, c):
        this_debt = c.get_this_debt(t)
        a = min(num, this_debt)
        p = a
        f =  a * self.radio
        inc = 0
        oid = 0
        if cn != '工资':
            self.fee += f
            inc = 1
            oid = cc.cid
        ll = cc.consume(t, p)
        if cn == '工资' and len(ll):
            inc = 2
            for v in ll:
                self.plan.append((t, cn, v[1], 0, c.get_name(),inc,v[0],c.cid))
        else:
            self.plan.append((t, cn, p, f, c.get_name(),inc,oid,c.cid))
        c.repay(a)
        if c.get_this_debt(t) < 0.01:
            return True
        return False

    def help_card(self, t, c):
        income = self.get_income(t)
        if income > 0 and self.transform_debt(t, self, '工资', income, c):
            return True
        readylist = []
        for cc in self.pool:
            if cc.name == c.name:
                continue
            if cc.should_cash_out(t):
                l = cc.limit * 0.9 - cc.debt
                readylist.append((cc.cid,cc.days_betw_next_repay(t),l))
        if len(readylist) == 0:
            return False
        sorted(readylist,key=lambda x: x[1],reverse=True)
        for cid in readylist:
            cc = self.get_card(cid[0])
            if self.transform_debt(t, cc, cc.name, cid[2], c):
                return True
        return False

    def check_repay(self, t):
        for c in self.pool:
            if not c.need_help(t):
                continue
            if c.is_over_date(t) and not c.load:
                c.load = True
                a = c.get_this_debt(t)
                self.plan.append((t - Day1, c.get_name(), a, 0, c.name,0,c.cid,c.cid))
            if not self.help_card(t, c):
                continue
