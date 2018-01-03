import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
# 模拟时间区间长度
t = 100
# 用户数
n = 50000
# 最高赔率
mr = 8.0
# 货币基金日收益率
r = 0.0365 / 365
# 竞猜中奖率
# ps = 0.90
# 模拟次数
pn = 30
# 复投比例
ir = 1.0
# 加速券票面利率
ar = 0.0365 / 365


# 一次完整的模拟
def inner_loop(m_t, m_p, m_n, fund, m_r, m_ar):
    # 用户的优联账户
    user_account = np.zeros((m_t, m_n))
    # 奖金池
    money_pool = 0.
    # 补贴账户
    allowance = 0.
    # 记录容器
    money_pool_radio = np.zeros(m_t)
    # 延迟收益
    dis_next = np.zeros(m_n)

    for i in range(1, m_t):
        # 中奖情况
        q = np.random.binomial(1, m_p, m_n)
        # 本次赌注
        a = user_account[i - 1] / ir + fund * m_r + dis_next
        user_account[i - 1] = user_account[i - 1] * (1 - 1.0 / ir)
        # 本次奖金
        s = float(np.sum(a)+money_pool)
        s2 = float(np.sum(a * q))
        if s2 == 0:
            user_account[i] = user_account[i - 1]
            money_pool += np.sum(a)
            print('No one Bingo this time: %d' % i)
            continue
        mc = min(s / s2, 8.0)
        # 赌注再分配
        k = mc * q * a
        user_account[i] = user_account[i - 1] + k
        # 赢得的钱尽量用来购买加速券（本金的万分之一与当前奖金取较小值）
        min_a = np.row_stack((np.floor(user_account[i]), np.ceil(fund/10000))).min(axis=0)
        # 累计补贴值
        allowance -= np.sum((10000*m_ar-1)*min_a)
        # 次日加速收益（延迟收益）
        dis_next = 10000*m_ar*min_a
        # 扣除买加速券的费用
        user_account[i] -= min_a
        # 剩余赌注归资金池
        money_pool = s - np.sum(k)
        # 记录器
        # money_pool_radio[i] = money_pool / (np.sum(fund) * r * i)
        # money_pool_radio[i] = money_pool
        money_pool_radio[i] = allowance

    return user_account, money_pool_radio, money_pool


# 多次模拟
def simulation_loop(ps=0.1):
    # 用户基金账户余额,不大于30000
    fund = np.random.exponential(3000, n)
    fund = np.where(fund > 30000, 30000, fund)
    set_radio_ts = np.zeros((t, pn))
    i = 0

    # pp = np.linspace(ps, 0.4, pn)
    # for p in pp:
    #     user_account, money_pool_radio, money_pool = inner_loop(t, p, n, fund, r, ar)
    #     set_radio_ts[:, i] = money_pool_radio
    #     i = i + 1

    ar_r = np.linspace(ar, 0.05/365, pn)
    for p_ar in ar_r:
        user_account, money_pool_radio, money_pool = inner_loop(t, ps, n, fund, r, p_ar)
        set_radio_ts[:, i] = money_pool_radio
        i = i + 1

    # 作图：在获奖率 p 下奖金池占比的时间序列
    # plot_money_pool_radio_ts(pp, set_radio_ts)
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
def balance_test(money_pool, user_account, fund, r, t):
    total = money_pool + np.sum(user_account[-1])
    fund_return = float(np.sum(fund) * r * (t - 1))
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
    plt.bar(pp, qq_mean / n, width)
    plt.ylabel('mean')
    plt.xlabel('p')
    plt.title('Money pool daily mean and std per custom')
    plt.subplot(212)
    plt.bar(pp, qq.std(axis=0) / n, width)
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
        plt.ylabel('p = %3.2f' % pp[ii])
        # plt.ylim([0, 1])

    plt.subplot(nn*100+11)
    # plt.title('Money Pool Radio of each day')
    # plt.title('Money Pool of each day')
    plt.title('Allowance of each day')
    plt.show()


# 作图：用户本金与最终受益对比
def plot_fund_user_account(fund, user_account):
    zz = np.zeros((N, 2))
    zz[:, 1] = fund.T
    zz[:, 0] = user_account[-1, :].T
    zz = zz[np.lexsort(-zz.T)]
    # 最后一天各用户收益情况
    plt.plot(zz[:, 0])
    plt.title('Profit of each custom(p = %5.2f)' % p)
    plt.show()
    # 用户初始金额
    plt.plot(zz[:, 1])
    plt.title('Initial Value of each custom(p = %5.2f)' % p)
    plt.show()


# 作图：在加速率 ar 和下补贴额的时间序列
def plot_allowance_surface(pp, money_pool_radio):
    fig = plt.figure(figsize=(8, 5))
    ax = Axes3D(fig)
    x = pp * 365 * 100
    y = np.arange(len(money_pool_radio[:, 0]))
    x, y = np.meshgrid(x, y)
    surf = ax.plot_surface(x, y, money_pool_radio, rstride=1, cstride=1, cmap='rainbow')
    ax.set_xlabel('Rate(%)')
    ax.set_ylabel('Time')
    ax.set_zlabel('Allowance')
    ax.set_title('Allowance of each day')
    ax.view_init(20, 10)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


def __main__():
    simulation_loop()


simulation_loop()
