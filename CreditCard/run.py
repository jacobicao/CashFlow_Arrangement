#!/usr/bin/env python
# encoding: utf-8
import csv
import pandas as pd
from Credit_card import Credit_card
from Card_pad import Card_pad, logger

def get_ic():
    iic = dict()
    try:
        with open('data/income.csv') as fi:
            fi.readline()
            reader = csv.reader(fi)
            for w in reader:
                t = pd.datetime(int(w[0]),int(w[1]),int(w[2]))
                iic[t] = int(w[3])
    except IOError as err:
        print('File error:'+str(err))
    return iic

def init_pad(pad):
    with open('data/card.csv') as fc:
        fc.readline()
        reader = csv.reader(fc)
        for row in reader:
            Credit_card(pad,row[0],int(row[1]),int(row[2]),int(row[3]))

    with open('data/now.csv') as fn:
        fn.readline()
        reader = csv.reader(fn)
        for w in reader:
            t = pd.datetime(int(w[1]),int(w[2]),int(w[3]))
            pad.get_card(w[0]).consume(t,int(w[4]))

def main():
    pad = Card_pad()
    init_pad(pad)
    iic = get_ic()
    rng = pd.date_range('2018-2-1','2018-12-31')
    for t in rng:
        if t in iic:
            pad.set_income(iic[t])
        pad.check_repay(t)
    logger.info('\n%s: 当前信用卡负债还有 %.f'%(t.date(),pad.get_total_debt()))
    logger.info('%s: 区间总手续费达 %.f\n'%(t.date(),pad.get_total_fee()))

if __name__ == "__main__":
    main()
