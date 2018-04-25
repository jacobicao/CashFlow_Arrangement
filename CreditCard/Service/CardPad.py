#!/usr/bin/env python
# encoding: utf-8
# from report import logger
from Service.Pad import Pad
import datetime as dt

Day1 = dt.timedelta(days=1)
format_er = '%s: %s - %.f -> %s'


class CardPad(Pad):
    def transform_debt(self, t, cc, cn, num, c):
        this_debt = c.get_this_debt(t.date())
        a = min(num, this_debt)
        # logger.info(format_er%(t.date(),cn,a,c.get_name()))
        self.plan.append((t.date(), cn, a, c.get_name()))
        cc.consume(t, a)
        c.repay(a)
        if cn != '工资':
            self.fee += a * 0.006
        if c.get_this_debt(t.date()) < 0.01:
            return True
        return False

    def help_card(self, t, c):
        if self.income > 0 and self.transform_debt(t, self, '工资', self.income, c):
            return True
        for cc in self.pool:
            if cc.name == c.name:
                continue
            if not cc.should_cash_out(t.date()):
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
                a = c.get_this_debt(t.date())
                # logger.info(format_er%(t.date()-Day1,'小额贷',a,c.name))
                self.plan.append((t.date() - Day1, '现贷', a, c.name))
            if not self.help_card(t, c):
                continue
