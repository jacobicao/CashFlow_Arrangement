#!/usr/bin/env python
# encoding: utf-8
import csv
import pandas as pd
from Credit_card import Credit_card
from Card_pad import Card_pad, logger

if __name__ == "__main__":
    pad = Card_pad()
    with open('card.csv') as fc:
        fc.readline()
        reader = csv.reader(fc)
        for row in reader:
            Credit_card(pad,row[0],int(row[1]),int(row[2]),int(row[3]))

    with open('now.csv') as fn:
        fn.readline()
        reader = csv.reader(fn)
        for w in reader:
            t = pd.datetime(int(w[1]),int(w[2]),int(w[3]))
            pad.get_card(w[0]).consume(t,int(w[4]))

    iic = dict()
    with open('income.csv') as fi:
        fi.readline()
        reader = csv.reader(fi)
        for w in reader:
            t = pd.datetime(int(w[0]),int(w[1]),int(w[2]))
            iic[t] = int(w[3])

    rng = pd.date_range('2018-2-1','2018-12-31')
    for t in rng:
        if t in iic:
            pad.set_income(iic[t])
        pad.check_repay(t)

    logger.info('\n%s: 当前总负债还有 %.f\n'%(t.date(),pad.get_total_debt()))
