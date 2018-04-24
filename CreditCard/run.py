#!/usr/bin/env python
# encoding: utf-8
import MyApi
import time



def main():
    uid = MyApi.input_user_name()
    B = False
    while(not B):
        p = input(MyApi.word)
        if p in MyApi.proc.keys():
            MyApi.proc[p](uid)
        elif p is 'e':
            B = True
            print('拜拜!\n')
        else:
            print('输入不对，再来一次!')
            time.sleep(3)


if __name__ == "__main__":
    main()
