import app.model.DAO.UserDao as UserDao


def log_on_user(s):
    UserDao.add_user(s)
    return UserDao.find_user(s)


def find_user_by_apikey(n):
    return UserDao.find_user(n)
