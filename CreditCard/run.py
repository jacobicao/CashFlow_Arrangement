#!/usr/bin/env python
# encoding: utf-8
import csv
import pandas as pd
from Credit_card import Credit_card
from Card_pad import Card_pad

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
            pad.get_card(w[0]).consume(pd.datetime(int(w[1]),int(w[2]),int(w[3])),int(w[4]))

    rng = pd.date_range('2018-2-1','2018-12-31')
    for t in rng:
        pad.check_repay(t)

    print('\n%s: 当前总负债还有 %.f\n'%(t.date(),pad.get_total_debt()))
