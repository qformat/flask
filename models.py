# -*- coding: utf-8 -*-
# created by K brother
from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表内容
    openid = db.Column(db.Text, nullable=True)
    rswsid = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)
    username = db.Column(db.Text, nullable=True)
    password = db.Column(db.Text, nullable=True)
    headimgurl = db.Column(db.Text, nullable=True)
    subscribe = db.Column(db.Text, nullable=True)
    subscribe_time = db.Column(db.Text, nullable=True)
    cishu = db.Column(db.Text, nullable=True)
    vip = db.Column(db.Text, nullable=True)
    uid = db.relationship('Message', backref='user', lazy='dynamic')


class Message(db.Model):
    __tablename__ = 'article_detail'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    msg = db.Column(db.Text, nullable=True)
    uid = db.Column(db.Integer, db.ForeignKey(User.id))


class Appid(db.Model):
    __tablename__ = 'appid'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表内容
    appid = db.Column(db.Text, nullable=True)
    secret = db.Column(db.Text, nullable=True)


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表内容
    token = db.Column(db.Text, nullable=True)


class Wlscan(db.Model):
    __tablename__ = 'wlscan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 表内容
    order = db.Column(db.Text, nullable=True)
    msg = db.Column(db.Text, nullable=True)
