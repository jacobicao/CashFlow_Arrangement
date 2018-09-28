# -*- coding: UTF-8 -*-
import os
from flask_script import Shell
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.model.DAO.DBTable import (User, Role, Permission,
                                   Card, Debt, Repay, Income, Incomego)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(db=db, User=User, Role=Role, Card=Card, Debt=Debt,
                Repay=Repay, Income=Income, Incomego=Incomego)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    Role.insert_roles()
    manager.run()
