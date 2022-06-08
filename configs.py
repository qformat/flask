# -*- coding: utf-8 -*-
# created by K brother

HOSTNAME = 'xxxxxxxxx'  # 数据库IP地址
PORT = '3306'  # 数据库端口
DATABASE = 'xxxx'  # 数据库库名
username = 'xxxxx'  # 数据库名
password = 'xxxxxx'  # 数据库密码
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(username, password,
                                                              HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
