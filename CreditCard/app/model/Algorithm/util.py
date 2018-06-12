# -*- coding: UTF-8 -*-
import datetime as dt


def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


def is_days(s):
    if not str(s).isdigit() or int(s)>30 or int(s)<1:
        return False
    return True


def is_date(s):
    if not isinstance(s,str):
        return False
    try:
        dt.datetime.strptime(s,'%Y-%m-%d')
    except ValueError:
        return False
    return True


def find_income(t,income):
    a = 0
    for v in income:
        if v[0] == t:
            break
        a += 1
    return a


def dateRange(beginDate, endDate):
    dates = []
    DB = dt.datetime.strptime(beginDate, "%Y-%m-%d")
    DE = dt.datetime.strptime(endDate, "%Y-%m-%d")
    m = 1
    t = DB
    while t <= DE:
        dates.append(t)
        t = datetime_offset_by_month(DB,m)
        m += 1
    return dates


def dateRange_by_days(DB,days):
    dates = []
    m = 1
    t = DB
    while m <= days:
        dates.append(t)
        t = t + dt.timedelta(1)
        m += 1
    return dates


def datetime_offset_by_month(datetime1, n = 1):
    one_day = dt.timedelta(days = 1)
    q,r = divmod(datetime1.month + n, 12)
    datetime2 = dt.datetime(datetime1.year + q, r + 1, 1) - one_day
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2
    if datetime1.day >= datetime2.day:
        return datetime2
    return datetime2.replace(day = datetime1.day)
