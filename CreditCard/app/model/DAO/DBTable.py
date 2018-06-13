# -*- coding: UTF-8 -*-
from datetime import datetime
from app import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app, request, url_for


class Permission:
    SEE = 1
    ADD = 2
    DELETE = 4
    PLAN = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.SEE, Permission.ADD,
                     Permission.DELETE, Permission.PLAN],
            'VIP': [Permission.SEE, Permission.ADD,
                    Permission.DELETE, Permission.PLAN],
            'Administrator': [Permission.SEE, Permission.ADD,
                              Permission.DELETE, Permission.PLAN,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    cards = db.relationship('Card', backref='user', lazy='dynamic')
    debts = db.relationship('Debt', backref='user', lazy='dynamic')
    repays = db.relationship('Repay', backref='user', lazy='dynamic')
    incomes = db.relationship('Income', backref='user', lazy='dynamic')
    incomegos = db.relationship('Incomego', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def generate_auth_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    A_day = db.Column(db.Integer)
    P_day = db.Column(db.Integer)
    num = db.Column(db.Float)
    on_use = db.Column(db.Boolean,default=True)
    ct = db.Column(db.Boolean,default=True)
    debts = db.relationship('Debt', backref='card', lazy='dynamic')
    repays = db.relationship('Repay', backref='card', lazy='dynamic')


class Debt(db.Model):
    __tablename__ = 'debts'
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    cid = db.Column(db.Integer, db.ForeignKey('cards.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Float)
    date = db.Column(db.Date)


class Repay(db.Model):
    __tablename__ = 'repays'
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    cid = db.Column(db.Integer, db.ForeignKey('cards.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Float)
    date = db.Column(db.Date)


class Income(db.Model):
    __tablename__ = 'incomes'
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Float)
    date = db.Column(db.Date)
    incomegos = db.relationship('Incomego', backref='income', lazy='dynamic')


class Incomego(db.Model):
    __tablename__ = 'incomegos'
    uid = db.Column(db.Integer, db.ForeignKey('users.id'))
    iid = db.Column(db.Integer, db.ForeignKey('incomes.id'))
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Float)
    date = db.Column(db.Date)
