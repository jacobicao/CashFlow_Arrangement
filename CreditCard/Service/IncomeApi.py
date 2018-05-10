import DAO.IncomeDao as IncomeDAO

# 收入类
def get_ic(uid):
    iic = dict()
    for v in IncomeDAO.find_income(uid):
        iic[v[0]] = int(v[1])
    return iic
