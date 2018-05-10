from DAO.DBConnect import DBSession
from sqlalchemy import Integer, Column, ForeignKey, CHAR, Date, Float
from sqlalchemy.ext.declarative import declarative_base
BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'user'
    uid = Column(Integer, primary_key=True)
    name = Column(CHAR(30))


class Card(BaseModel):
    __tablename__ = 'card'
    cid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.uid'))
    name = Column(CHAR(30))
    A_day = Column(Integer)
    P_day = Column(Integer)
    num = Column(Float)
    on_use = Column(Integer,default=1)


class Debt(BaseModel):
    __tablename__ = 'debt'
    uid = Column(Integer, ForeignKey('user.uid'))
    cid = Column(Integer, ForeignKey('card.cid'))
    did = Column(Integer, primary_key=True)
    num = Column(Float)
    P_time = Column(Date)
    paidoff = Column(Integer,default=0)


class Repay(BaseModel):
    __tablename__ = 'repay'
    uid = Column(Integer, ForeignKey('user.uid'))
    cid = Column(Integer, ForeignKey('card.cid'))
    rid = Column(Integer, primary_key=True)
    num = Column(Float)
    P_time = Column(Date)


class Income(BaseModel):
    __tablename__ = 'income'
    uid = Column(Integer, ForeignKey('user.uid'))
    iid = Column(Integer, primary_key=True)
    num = Column(Float)
    P_time = Column(Date)


class Incomego(BaseModel):
    __tablename__ = 'incomego'
    uid = Column(Integer, ForeignKey('user.uid'))
    iid = Column(Integer, ForeignKey('income.iid'))
    gid = Column(Integer, primary_key=True)
    num = Column(Float)
    P_time = Column(Date)

# initial database
def init_db():
    BaseModel.metadata.create_all(DBSession.get())


def drop_db():
    BaseModel.metadata.drop_all()


if __name__ == '__main__':
    init_db()
