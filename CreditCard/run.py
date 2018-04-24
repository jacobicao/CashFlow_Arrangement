#!/usr/bin/env python
# encoding: utf-8
import MyApi

def input_user_name():
    uid = MyApi.find_user_id(input('Input user name:'))
    while(uid == 0):
        print('User name does not exist!')
        uid = MyApi.find_user_id(input('Input user name:'))
    return uid

def show_plan(uid):
    dt = '2018-02-01'
    pad = MyApi.get_pad()
    MyApi.init_pad(pad,uid)
    iic = MyApi.get_ic(uid)
    plan = MyApi.cal_plan(pad,iic,dt)
    plan.to_csv('log/Cash_out_plan.csv',float_format='%d')
    print(plan)

def show_debt(uid):
    MyApi.debt_list(uid)
    
def is_float(str):
    try:     
        f = float(str) 
    except ValueError:     
        return False
    return True

def add_debt(uid):
    MyApi.card_list(uid)
    cid = input('Which card?')
    dt = input('When happen?')
    num = input('How many?')
    while(not is_float(num)):
        print('Not a number')
        num = input('How many?')
    try:
        MyApi.add_ont_debt(uid,cid,dt,num)
    except Exception as e:
        print('Error input:',e)
    except:
        print('Error input!')
    else:
        print('Success!')

def delete_debt(uid):
    l = MyApi.debt_list(uid)
    did = int(input('Which debt?'))
    if not did in l:
        print('Error input!')
        return
    MyApi.delete_one_debt(uid,did)
    print('Success!')

proc = dict({'1':show_plan,'2':show_debt,'3':add_debt,'4':delete_debt})
word = '\n(1)Show plan\n(2)Show debt\n(3)Add debt\n(4)Delete debt\n(e)xit\nPlease input:'

def main():
    uid = 1#input_user_name()
    B = False
    while(not B):
        p = input(word)
        if p in proc.keys():
            proc[p](uid)
        elif p is 'e':
            B = True
            print('Bye bye!\n')
        else:
            print('Error input!\n')


if __name__ == "__main__":
    main()
