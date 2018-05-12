#!/usr/bin/env python
# encoding: utf-8
# from report import logger
from Algorithm.Pad import Pad
import datetime as dt

Day1 = dt.timedelta(days=1)

class CardPad(Pad):
    def transform_debt(self, t, cc, cn, num, c):
        this_debt = c.get_this_debt(t)
        a = min(num, this_debt)
        p = a
        inc = 0
        oid = 0
        if cn != '工资':
            p = round(a*(1+self.radio),2)
            self.fee += a * self.radio
            inc = 1
            oid = cc.cid
        ll = cc.consume(t, p)
        if cn == '工资' and len(ll):
            inc = 2
            for v in ll:
                self.plan.append((t, cn, v[1], c.get_name(),inc,v[0],c.cid))
        else:
            self.plan.append((t, cn, p, c.get_name(),inc,oid,c.cid))
        c.repay(a)
        if c.get_this_debt(t) < 0.01:
            return True
        return False

    def help_card(self, t, c):
        income = self.get_income(t)
        if income > 0 and self.transform_debt(t, self, '工资', income, c):
            return True
        for cc in self.pool:
            if cc.name == c.name:
                continue
            if not cc.should_cash_out(t):
                continue
            if self.transform_debt(t, cc, cc.name, cc.limit * 0.9 - cc.debt, c):
                return True
        return False

    def check_repay(self, t):
        for c in self.pool:
            if not c.need_help(t):
                continue
            if c.is_over_date(t) and not c.load:
                c.load = True
                a = c.get_this_debt(t)
                self.plan.append((t - Day1, '现金贷', a, c.name,0,c.cid,c.cid))
            if not self.help_card(t, c):
                continue
