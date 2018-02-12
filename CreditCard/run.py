#!/usr/bin/env python
# encoding: utf-8
import csv
import pandas as pd
from Credit_card import Credit_card
from Card_pad import Card_pad

if __name__ == "__main__":
    pad = Card_pad()
    with open('card.csv') as fc:
        reader = csv.reader(fc)
        for row in reader:
            Credit_card(pad,row[0],int(row[1]),int(row[2]),int(row[3]),0)

    rng = pd.date_range('2018-2-1','2018-12-31')
    pad.get_card('中行J').consume(pd.datetime(2018,1,20),13000)
    pad.get_card('平安J').consume(pd.datetime(2018,1,20),27000)
    pad.get_card('中信J').consume(pd.datetime(2018,2,1),13000)
    pad.get_card('农行J').consume(pd.datetime(2018,2,1),5300)
    pad.get_card('建设Q').consume(pd.datetime(2018,1,20),39000)
    pad.get_card('中行Q').consume(pd.datetime(2018,1,20),25000)

    for t in rng:
        pad.check_repay(t)

    print('\n%s: 当前总负债还有 %.f'%(t.date(),pad.get_total_debt()))
