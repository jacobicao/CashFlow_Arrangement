from .DBTable import User
from .DBConnect import DBSession


def add_user(s):
    session = DBSession()
    stu = User(name=s)
    session.add(stu)
    session.commit()
    session.close()


def delete_user(s):
    session = DBSession()
    query = session.query(User.name)
    query.filter(User.name == s).delete()
    session.commit()
    session.close()


def find_user(s):
    session = DBSession()
    query = session.query(User.uid)
    uid = query.filter(User.name == s).first()
    session.close()
    if uid is None:
        return 0
    return uid[0]


def con_user(u,s):
    session = DBSession()
    query = session.query(User.uid)
    uid = query.filter(User.uid == u, User.name == s).first()
    session.close()
    if uid is None:
        return False
    return True
