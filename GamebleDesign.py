#!/usr/bin/env python
# -*- coding: utf-8 -*

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 模拟时间区间长度
t = 100
# 用户数
n1 = 50000
n2 = 100000
# 最高赔率
mr = 8.0
# 首日补贴年化收益率
fr = 0.04
# 人头补贴
ah = 1.0
# 模拟次数
pn = 10
# 复投比例
ir = 0.65
# 加速券票面年化利率
ar = 0.0365


# 一次完整的模拟
def inner_loop(m_t, m_p, m_d, m_n1, m_n2, fund, m_r, m_ar):
    """
    :param m_t: 时间长度
    :param m_p: 中奖概率
    :param m_d: 复投比例
    :param m_n1: 初始人数
    :param m_n2: 最终人数
    :param fund: 初始资金
    :param m_r: 初次竞猜补贴比例
    :param m_ar: 加速券利息率
    :return: 每日补贴额
    """
    # 每日用户数
    user_number = np.linspace(m_n1, m_n2, m_t).astype(int)
    # 用户的优联账户
    user_account = np.zeros((m_t, m_n2))
    # 奖金池
    money_pool = 0.
    # 总补贴
    allowance = 0.
    # 记录容器
    money_pool_radio = np.zeros(m_t)
    # 奖金取出
    record_d = 0.
    # 加速券总收入
    record_a = 0.

    # Day1
    min_a = fund[:user_number[0]]//1000/10  # 买加速券的情况（最小单位0.1元）
    record_a += np.sum(min_a)
    allowance = allowance - (money_pool
                             + user_number[0]*ah  # 新用户人头补贴
                             + np.sum(fund[:user_number[0]])*m_r/365  # 新用户的本金补贴
                             + np.sum(min_a)*(m_ar/365*10000-1))  # 加速券补贴
    s = abs(allowance) + np.sum(min_a)
    a = fund[:user_number[0]]*m_r/365 + min_a*m_ar/365*10000

    for i in range(1, m_t):
        # 中奖情况
        q = np.random.binomial(1, m_p, user_number[i-1])
        s2 = float(np.sum(a * q))
        if s2 == 0:
            user_account[i] = 0
            money_pool += s
            print('No one Bingo this time: %d' % i)
            continue
        mc = min(s / s2, 8.0)
        # 赌注再分配
        k = mc * q * a
        # 剩余赌注归资金池
        money_pool = s - np.sum(k)
        # 复投情况
        d = np.random.binomial(1, m_d, user_number[i-1])
        user_account[i][:user_number[i - 1]] = k*d
        # 奖金取出
        fund[:user_number[i-1]] += k*(1-d)
        record_d += np.sum(k*(1-d))
        # 当日下注
        min_a = (np.append(d, np.ones(user_number[i]-user_number[i-1])) *
                 fund[:user_number[i]])//1000/10  # 买加速券的情况（最小单位0.1元）,而且不复投不能买加速券
        record_a += np.sum(min_a)
        a = (user_account[i][:user_number[i]]  # 旧用户复投
             + np.append(np.zeros(user_number[i - 1]), fund[user_number[i - 1]: user_number[i]])*m_r/365  # 新用户首次加息
             + min_a*m_ar/365*10000)  # 加速券
        # 平衡试算
        # money_pool_radio[i] = \
        #    (record_a - np.sum(min_a)) + abs(allowance) - money_pool - record_d - (np.sum(user_account[i]))  # 平衡试算
        # 下次奖金
        money_pool += (user_number[i] - user_number[i - 1]) * ah
        s = float(np.sum(a)+money_pool)
        # 累计补贴值
        allowance = allowance - (
                np.sum(fund[user_number[i-1]:user_number[i]])*m_r/365  # 新增本金补贴
                + np.sum(min_a)*(10000*m_ar/365-1)  # 加速券补贴
                + (user_number[i]-user_number[i-1])*ah)  # 新增人头补贴

        # 记录器
        # money_pool_radio[i] = money_pool / (np.sum(fund) * r * i)
        money_pool_radio[i] = allowance + money_pool

    return money_pool_radio


# 多次模拟
def simulation_loop(ps=0.125):
    # 用户基金账户余额,不大于30000
    fund = np.random.exponential(3000, n2)
    fund = np.where(fund > 30000, 30000, fund)
    set_radio_ts = np.zeros((t, pn))
    i = 0

    ar_r = np.linspace(ar, 0.04, pn)
    for p_ar in ar_r:
        money_pool_radio = np.zeros(t)
        for k in range(20):
            money_pool_radio += inner_loop(t, ps, ir, n1, n2, fund, fr, p_ar)
        set_radio_ts[:, i] = money_pool_radio/20
        i = i + 1

    # 作图：在获奖率 p 下奖金池占比的时间序列
    # plot_money_pool_radio_ts(ar_r, set_radio_ts)
    # 作图：在获奖率 p 下奖金池日净流入的均值标准差
    # plot_money_pool_mean_std(pp, set_radio_ts)
    # 平衡试算
    # balance_test(money_pool, user_account, fund, r, t)
    # 作图：用户本金与最终受益对比
    # plot_fund_user_account(fund, user_account)
    # 作图：不同 p 下的奖金池占比(投注总额)
    # plot_money_pool_radio_pp(pp, set_radio_ts)
    # 作图：在加速率 ar 和下补贴额的时间序列
    plot_allowance_surface(ar_r, set_radio_ts)


# 平衡试算
def balance_test(money_pool, user_account, fund, m_r, m_t):
    total = money_pool + np.sum(user_account[-1])
    fund_return = float(np.sum(fund) * m_r * (m_t - 1))
    print('Total dynamic profit is %9.2f' % total)
    print('Total Fund profit is %9.2f' % fund_return)


# 作图：不同 p 下的奖金池占比(投注总额)
def plot_money_pool_radio_pp(pp, money_pool_radio):
    nn = len(pp)
    if nn > 9:
        print('It is too much time series!')
        return

    plt.figure(figsize=(8, 5))
    for ii in range(nn):
        poc = int(nn * 100 + 10 + ii + 1)
        plt.subplot(poc)
        plt.plot(money_pool_radio[:, ii])
        plt.ylabel('p = %3.2f' % pp[ii])
        plt.ylim([0, 1])

    plt.subplot(nn * 100 + 11)
    plt.title('Money Pool Radio of each day')
    plt.show()


# 作图：在获奖率 p 下奖金池日净流入的均值标准差
def plot_money_pool_mean_std(pp, money_pool_radio):
    plt.figure(figsize=(8, 5))
    width = (pp[-1]-pp[0])/len(pp)
    plt.subplot(211)
    qq = np.diff(money_pool_radio, axis=0)
    x = np.arange(len(money_pool_radio[:, 0]))
    qq_mean = np.zeros(len(pp))
    for ii in range(len(pp)):
        qq_mean[ii] = np.polyfit(x, money_pool_radio[:, ii], deg=1)[0]
    plt.bar(pp, qq_mean / n2, width)
    plt.ylabel('mean')
    plt.xlabel('p')
    plt.title('Money pool daily mean and std per custom')
    plt.subplot(212)
    plt.bar(pp, qq.std(axis=0) / n2, width)
    plt.ylabel('std')
    plt.xlabel('p')
    plt.show()


# 作图：在获奖率 p 下奖金池占比的时间序列
def plot_money_pool_radio_ts(pp, money_pool_radio):
    nn = len(pp)
    if nn > 9:
        print('It is too much time series!')
        return

    plt.figure(figsize=(8, 5))
    for ii in range(nn):
        poc = int(nn*100+10+ii+1)
        plt.subplot(poc)
        plt.plot(money_pool_radio[:, ii])
        x = np.arange(len(money_pool_radio[:, ii]))
        reg = np.polyfit(x, money_pool_radio[:, ii], deg=1)
        ry = np.polyval(reg, x)
        plt.plot(ry, 'r-')
        plt.ylabel('%3.2f%%' % (pp[ii]*100))

    plt.subplot(nn*100+11)
    # plt.title('Money Pool Radio of each day')
    # plt.title('Money Pool of each day')
    plt.title('Allowance + Pool (Recast=%.2f)' % ir)
    plt.show()


# 作图：用户本金与最终受益对比
def plot_fund_user_account(fund, user_account):
    zz = np.zeros((n2, 2))
    zz[:, 1] = fund.T
    zz[:, 0] = user_account[-1, :].T
    zz = zz[np.lexsort(-zz.T)]
    # 最后一天各用户收益情况
    plt.plot(zz[:, 0])
    plt.title('Profit of each custom(p = %5.2f)' % ir)
    plt.show()
    # 用户初始金额
    plt.plot(zz[:, 1])
    plt.title('Initial Value of each custom(p = %5.2f)' % ir)
    plt.show()


# 作图：在加速率 ar 和下补贴额的时间序列
def plot_allowance_surface(pp, money_pool_radio):
    fig = plt.figure(figsize=(8, 5))
    ax = Axes3D(fig)
    x = pp * 100
    y = np.arange(len(money_pool_radio[:, 0]))
    x, y = np.meshgrid(x, y)
    surf = ax.plot_surface(x, y, money_pool_radio, rstride=1, cstride=1, cmap='rainbow')
    ax.set_xlabel('Rate(%)')
    ax.set_ylabel('Time')
    ax.set_zlabel('Net')
    ax.set_title('Allowance + Pool (Recast=%.2f)' % ir)
    ax.view_init(15, 60)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def __main__():
    simulation_loop()


simulation_loop()
