import pandas as pd
from Service.CardService import *
from Service.UserService import *
from Service.IncomeService import *
from Service.DebtService import *
from Service.PadService import *


record_program = {'1': show_plan,
                  '2': debt_list,
                  '3': add_one_debt,
                  '4': delete_one_debt,
                  '5': add_one_card,
                  '6': delete_one_card,
                  }
record_word = '\n' \
              '(1)查看计划\n'        \
              '(2)查看当前账单\n'     \
              '(3)增加一条刷卡记录\n'  \
              '(4)删除一条刷卡记录\n'  \
              '(5)增加一张卡片\n'     \
              '(6)删除一张卡片\n'     \
              '(e)退出\n'            \
              '请输入:'


login_program = {'1': lambda f: f(input_user_name()),
                 '2': lambda f: f(log_on_user(input('请输入用户名:')))}
login_word = '\n'       \
             '(1)登录\n' \
             '(2)注册\n' \
             '(e)退出\n' \
             '请输入:'


def general_logic(word, program, x):
    import time
    b = True
    while b:
        p = input(word)
        if p in program.keys():
            program[p](x)
        elif p is 'e':
            b = False
            print('拜拜!\n')
        else:
            print('输入不对，再来一次!')
            time.sleep(3)
