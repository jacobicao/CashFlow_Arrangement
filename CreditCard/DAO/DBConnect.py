from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
DB_name = 'sa'
DB_P = '1234'
DB_AD = 'localhost'
DB_DB = 'credit_card_system'
DB_CARR_SET = 'charset=utf8'
DB_CONNECT = DB_name + ':' + DB_P + '@' + DB_AD + '/' + DB_DB + '?' + DB_CARR_SET


class DBC:
    def __init__(self,type = 1):
        if type == 1:
            self.engine_name = "mysql+mysqlconnector://"+DB_CONNECT
        elif type == 2:
            import os
            if not os.path.exists('data'):
                os.mkdir('data')
            self.engine_name = 'sqlite:///data/cds.db'
        else:
            raise Exception('Error database type!')
        self.engine = create_engine(self.engine_name,echo=True)
        self.DBSession = sessionmaker(bind=self.engine)

    def __call__(self):
        return self.DBSession()

    def get(self):
        return self.engine


DBSession = DBC(2)
