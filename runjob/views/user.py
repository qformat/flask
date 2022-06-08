# -*- coding: utf-8 -*-
# created by K brother

import re
from flask import Blueprint, redirect
from flask import request, render_template, flash, session, url_for
from exts import db
from models import User, Appid
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)


@user.route('/login/', methods=['GET', 'POST'])  # 登录页面
def login():
    user = session.get('username')  # 获取用户登录session
    if user is not None:
        return render_template('error.html', erro='错误！您已经登录了，请不要重复登录！')

    form = request.form
    # 获取表单提交的用户名密码
    username = form.get('username')
    password = form.get('password')
    # 查找用户名对应的第一个用户
    user_in = db.session.query(User).filter_by(username=username).first()
    appid = Appid.query.get(1)
    print(appid.appid, appid.secret)
    # 判断user是否为空，否则会报错
    if user_in is None:
        flash('用户名或密码错误')
        return render_template('login.html')
    else:
        print(user_in.username, user_in.password)
        # 判断用户名 和解密后的密码是否一致 如果一致那么跳转到index.html
        if username == user_in.username and check_password_hash(str(user_in.password), str(password)) is True:
            session['username'] = username  # 写入session
            return redirect('/')
        else:
            flash('用户名或密码错误')
            return render_template('login.html')


@user.route('/reg/', methods=['GET', 'POST'])  # 注册页面
def reg():
    form = request.form
    username = form.get('Name')
    password = form.get('Password')
    password2 = form.get('Password2')
    email = form.get('Email')
    rules = r'[\u4e00-\u9fa5]'
    user_first = User.query.filter(User.username == username).first()  # 查询数据库返回第一条数据
    if not username:
        flash('请输入用户名')
        return render_template("reg.html")
    if len(username) <= 5:
        flash('用户名不能太短')
    if len(username) >= 16:
        flash('用户名不能太长')
    if re.search(rules, username):
        flash('只能输入英文加数字')
    if not password:
        flash('请输入密码')
        return render_template('reg.html')
    if password != password2:
        flash('两次密码不一致')
    if user_first is not None:
        flash('用户名已存在')
        return render_template('reg.html')
    else:
        pass_word = generate_password_hash(password)  # 密码加密
        user_reg = User(username=username, password=pass_word, email=email)
        print(user_reg)
        db.session.add(user_reg)
        db.session.commit()  # 写入数据库
        return redirect('/login/')


@user.route('/error/')
def error():
    return render_template('error.html')
