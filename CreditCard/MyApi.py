from Service.CardService import *
from Service.UserService import *
from Service.IncomeService import *
from Service.DebtService import *
from Service.PadService import *
from Service.RepayService import *


record_program = {'1': show_plan,
                  '2': debt_list,
                  '3': add_one_debt,
                  '4': delete_one_debt,
                  '5': card_list,
                  '6': add_one_card,
                  '7': delete_one_card,
                  '8': income_list,
                  '9': add_one_income,
                  '10': delete_one_income,
                  '11': delete_one_incomego,
                  '12': repay_list,
                  '13': add_one_repay,
                  '14': delete_one_repay,
                  '15': cal_debt_current,
                  '16': load_list,
                  '17': add_loan,
                  '18': delete_load,
                  }
record_word = '\n' \
              '(1)查看计划\n'         \
              '(2)查看所有刷卡记录\n'  \
              '(3)增加一条刷卡记录\n'  \
              '(4)删除一条刷卡记录\n'  \
              '(5)查看所有卡片\n'     \
              '(6)增加一张卡片\n'     \
              '(7)删除一张卡片\n'     \
              '(8)查看所有收入\n'     \
              '(9)增加一条收入\n'     \
              '(10)删除一条收入\n'    \
              '(11)删除一条支出\n'    \
              '(12)查看所有还款记录\n' \
              '(13)增加一条还款记录\n' \
              '(14)删除一条还款记录\n' \
              '(15)查看当前账单列表\n' \
              '(16)查看贷款记录\n'    \
              '(17)增加贷款记录\n'    \
              '(18)删除贷款记录\n'    \
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
