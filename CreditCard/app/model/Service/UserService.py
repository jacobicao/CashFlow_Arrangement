import app.model.DAO.UserDao as UserDao


def log_on_user(s):
    UserDao.add_user(s)
    return UserDao.find_user(s)


def input_user_name(n):
    uid = UserDao.find_user(n)
    if not uid:
        print('用户名不存在!')
    return uid


def queding(u,s):
    return UserDao.con_user(u,s)
