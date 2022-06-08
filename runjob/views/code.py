# -*- coding: utf-8 -*-
# created by K brother
import json
import requests
from flask import Blueprint, session, redirect, request, render_template
from models import Appid, User, Token
from exts import db
import uuid

code = Blueprint('code', __name__)


@code.route('/code/', methods=['POST', 'GET'])  # 获取code页面
def blue_code():
    appid_in = Appid.query.get(1)
    appid = appid_in.appid
    secret = appid_in.secret
    scope = 'snsapi_userinfo'
    print(appid)
    username = request.args.get('username')
    redirect_url = f'http%3A//wxapi.rsws.top/qr/'
    source_url = 'https://open.weixin.qq.com/connect/oauth2/authorize' \
                 + '?&appid={APPID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&state={STATE}' \
                 + '#wechat_redirect'
    url = source_url.format(APPID=appid, REDIRECT_URI=redirect_url, SCOPE=scope, STATE=username)
    return redirect(url)  # 重定向


@code.route('/qr/', methods=['POST', 'GET'])  # 手机端获取code页面
def blue_qr():
    appid_in = Appid.query.get(1)  # 读取数据库
    appid = appid_in.appid  # 读取数据库里的appid和secret
    secret = appid_in.secret
    code = request.args.get('code')  # 抓取跳转页面返回的code值
    username = request.args.get('state')  # 抓取跳转页面返回的username，state字段是唯一可以返回的url参数
    url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={str(code)}&grant_type=authorization_code'
    resp = requests.get(url)
    datacode = resp.text
    resp_dict3 = json.loads(datacode)
    if 'openid' in resp_dict3:  # 判断openid字段是否存在在变量中
        openid = resp_dict3['openid']
        token1 = Token.query.order_by(Token.id.desc()).first()
        if token1 is None:  # 判断token是否存在，如果不存在则运行token()，生成一个新的tonken
            token()
            token1 = Token.query.order_by(Token.id.desc()).first()
            token1 = str(token1.token)
        get_userinfo = f'https://api.weixin.qq.com/cgi-bin/user/info?access_token={token1.token}&openid={openid}&lang=zh_CN'
        resp2 = requests.get(get_userinfo)
        datacode1 = resp2.text
        resp_dict4 = json.loads(datacode1)
        if 'errcode' in resp_dict4:  # 判断errcode字段是否存在在变量中，errcode报错42001的话说明token过期，需要运行token()重新申请新的。
            if resp_dict4['errcode'] == 42001:
                token()
                token1 = Token.query.order_by(Token.id.desc()).first()
                token1 = str(token1.token)
                get_userinfo = f'https://api.weixin.qq.com/cgi-bin/user/info?access_token={token1}&openid={openid}&lang=zh_CN'
                resp2 = requests.get(get_userinfo)
                datacode1 = resp2.text
                resp_dict4 = json.loads(datacode1)
    else:
        return render_template('qr.html')
    openid = resp_dict4['openid']  # 获取到openid
    subscribe = resp_dict4['subscribe']  # 获取到 subscibe 这个字段是判断用户是否关注了公众号，1带表关注，0代表未关注。
    subscribe_time = resp_dict4['subscribe_time']  # 获取到 subscibe_time 这个字段是用户关注的时间
    user_in = db.session.query(User).filter_by(username=username).first()  # first返回的是对象(因为就一个)
    if subscribe != 1:  # 判断如果没有关注公众号则运行qr.html
        return render_template('qr.html')
    else:
        wsid = uuid.uuid1()
        uid = wsid.hex
        rswsid = 'RSWS' + uid[1:20]
        user_in.openid = openid  # 写入openid到数据库
        user_in.subscribe = subscribe
        user_in.subscribe_time = subscribe_time
        user_in.rswsid = rswsid
        db.session.commit()  # 数据库提交
        return render_template('qr.html')


def token():  # 生成token，生成后存储到数据库。
    appid_in = Appid.query.get(1)
    appid = appid_in.appid
    secret = appid_in.secret
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(
        appid, secret)
    ret = requests.get(url=url)
    content = ret.content.decode("utf-8")
    js = json.loads(content)
    access_token = js['access_token']
    token = Token(token=access_token)
    db.session.add(token)
    db.session.commit()
    return access_token
