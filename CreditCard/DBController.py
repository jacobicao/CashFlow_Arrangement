from DBConnect import DBSession
from sqlalchemy import Integer,Column, String, ForeignKey, CHAR, Date, Float
from sqlalchemy.ext.declarative import declarative_base
BaseModel = declarative_base()


class User(BaseModel):
    __tablename__='user'
    uid = Column(Integer,primary_key = True)
    name = Column(CHAR(30))


class Card(BaseModel):
    __tablename__='card'
    cid = Column(Integer,primary_key = True)
    uid = Column(Integer,ForeignKey('user.uid'))
    name = Column(CHAR(30))
    A_day = Column(Integer)
    P_day = Column(Integer)
    num = Column(Float)


class Debt(BaseModel):
    __tablename__ = 'debt'
    uid = Column(Integer,ForeignKey('user.uid'))
    cid = Column(Integer,ForeignKey('card.cid'))
    did = Column(Integer,primary_key=True)
    num = Column(Float)
    P_time = Column(Date)


class Income(BaseModel):
    __tablename__ = 'income'
    uid = Column(Integer,ForeignKey('user.uid'))
    iid = Column(Integer,primary_key=True)
    num = Column(Float)
    P_time = Column(Date)


# 用户
def add_user(s):
    session = DBSession()
    stu = User(name = s)
    session.add(stu)
    session.commit()
    session.close()

def delete_user(s):
    session = DBSession()
    query = session.query(User.name)
    query.filter(User.name==s).delete()
    session.commit()
    session.close()

def find_user(s):
    session = DBSession()
    query = session.query(User.uid)
    id = query.filter(User.name==s).first()[0]
    session.close()
    return id

# 卡
def add_card(u,s,a,p,f):
    session = DBSession()
    card = Card(uid = u, name = s, A_day = a, P_day = p, num = f)
    session.add(card)
    session.commit()
    session.close()

def delete_card(c):
    session = DBSession()
    query = session.query(Card.cid)
    query.filter(Card.cid==c).delete()
    session.commit()
    session.close()

def find_card(u):
    session = DBSession()
    query = session.query(Card.cid,Card.A_day,Card.P_day,Card.num)
    re = query.filter(Card.uid==u).all()
    session.close()
    return re

# 债
def add_debt(u,c,t,n):
    session = DBSession()
    id = session.query(Card.cid).filter(Card.name==c)
    debt = Debt(uid = u, cid = id, P_time=t,num=n)
    session.add(debt)
    session.commit()
    session.close()

def delete_debt(d):
    session = DBSession()
    query = session.query(Debt.did)
    query.filter(Debt.did==d).delete()
    session.commit()
    session.close()

def find_debt(u):
    session = DBSession()
    query = session.query(Debt.cid,Debt.P_time,Debt.num)
    re = query.filter(Debt.uid==u).all()
    session.close()
    return re


# 收入
def add_income(u,t,n):
    session = DBSession()
    income = Income(uid=u,P_time=t,num=n)
    session.add(income)
    session.commit()
    session.close()

def delete_income(i):
    session = DBSession()
    query = session.query(Income.iid)
    query.filter(Income.iid==i).delete()
    session.commit()
    session.close()

def find_income(u):
    session = DBSession()
    query = session.query(Income.P_time,Income.num)
    re = query.filter(Debt.uid==u).all()
    session.close()
    return re


# initial database
def init_db():
    BaseModel.metadata.create_all(DBSession.get())

def drop_db():
    BaseModel.metadata.drop_all()


if __name__ == '__main__':
    init_db()
