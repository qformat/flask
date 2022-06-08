# -*- coding: utf-8 -*-
# created by K brother

# 首页面展示
import uuid
from flask import render_template, Blueprint, session, redirect
from models import User
from exts import db
from MyQR import myqr
import random

show = Blueprint('show', __name__)


@show.route('/')  # 首页面
def index():
    user = session.get('username')  # 获取用户登录session
    if user is None:  # 如果用户没有登录则提示
        print('未获取到session')
        qrcode = '/static/qrcode/gz.png'
        return render_template('index.html', gz='请扫码关注公众号后再注册登录！', qrcode=qrcode)

    else:

        user_in = db.session.query(User).filter_by(username=user).first()  # 读取用户数据库数据

        if user_in.subscribe != '1':  # 判断用户是否关注了公众号

            return redirect('/qrcode/')  # 如果用户没有关注公众号则重定向到扫码页面

        else:
            qrcode = '/static/qrcode/tm.png'
            rswsid = user_in.rswsid  # 从数据库获取到用户openid
            session['rswsid'] = rswsid
            return render_template('index.html', out='退出登录', echo=f'您的RswsID是：\n{rswsid}', wel=f'欢迎用户【{user}】',
                                   rest='重置RswsID',
                                   qrcode=qrcode)


@show.route('/rest')
def rest():
    user = session.get('username')
    user_in = db.session.query(User).filter_by(username=user).first()  # 读取用户数据库数据
    wsid = uuid.uuid1()
    uid = wsid.hex
    rswsid = 'RSWS' + uid[1:20]
    user_in.rswsid = rswsid
    session['rswsid'] = rswsid
    db.session.commit()  # 数据库提交
    qrcode = '/static/qrcode/tm.png'

    return render_template('index.html', out='退出登录', echo=f'您的RswsID是：\n{rswsid}', wel=f'欢迎用户【{user}】',
                           rest='重置RswsID',
                           qrcode=qrcode)


@show.route('/qrcode/')  # 扫码跳转页
def qrcode():
    user = session.get('username')
    if user is None:
        return render_template('index.html')
    # user_in = db.session.query(User).filter_by(username=user).first()
    qr = str(random.randint(500, 99999))
    myqr.run(words=f'http://wxapi.rsws.top/code?username={user}',
             version=6,
             save_name=f'{qr}.jpg',
             save_dir='static/images/')
    qrcode = f'\static\images\{qr}.jpg'

    return render_template('qrcode.html', qrcode=qrcode)


@show.route("/dataFromAjax", methods=['GET'])  # 判断ajax 是否获取到了用户扫码信息
def recv():
    user = session.get('username')
    user_in = db.session.query(User).filter_by(username=user).first()
    if user is None:
        print('等待用户登录')
        return '2'
    else:
        if user_in.subscribe == '1':
            return "1"
        else:
            print("等待用户扫码")
            return "0"


@show.route('/logout/', methods=['POST', 'GET'])  # 退出登录
def logout():
    session.pop('username', None)
    session.pop('rswsid', None)

    return redirect('/')


@show.route('/state/', methods=['POST', 'GET'])  # 说明页面
def bulu_state():
    return render_template('state.html')
