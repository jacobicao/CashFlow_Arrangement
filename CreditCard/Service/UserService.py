import DAO.UserDao as UserDao

# 用户类
def log_on_user(s):
    UserDao.add_user(s)
    print('注册成功')
    return UserDao.find_user(s)


def input_user_name():
    uid = UserDao.find_user(input('输入用户名:'))
    if not uid:
        print('用户名不存在!')
    return uid
