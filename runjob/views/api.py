# -*- coding: utf-8 -*-
# created by K brother

# 首页面展示
import datetime
import json
import requests
from flask import render_template, Blueprint, session, request, url_for
from models import Token, Appid, User, Message
from exts import db

api = Blueprint('api', __name__)


@api.route('/api/')  # api页面
def blue_api():
    rswsid = session.get('rswsid')
    if rswsid is None:
        rswsid = '您还没有登录，或尚未绑定RswsID'
    return render_template('api.html', rswsid=rswsid)


@api.route('/apisend/', methods=['POST', 'GET'])  # api发送页面
def blue_apisend():
    time_lite = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # form = request.form
    # 获取表单提交的标题和内容
    rswsid = request.args.get('rswsid')
    uid = db.session.query(User).filter_by(rswsid=rswsid).first()
    openid = uid.openid
    title = request.args.get('title')
    msg = request.args.get('msg')
    print(openid, title, msg)

    params = ({'touser': f"{openid}",  # 用户openid
               'template_id': 'xxxxxxxxxx',  # 模板消息ID
               'url': f'//wxapi.rsws.top/msg/?title={title}&msg={msg}',  # 跳转链接
               "topcolor": "#667F00",  # 颜色
               "data": {  # 模板内容
                   "first": {"value": f"{title}", "color": "#ffffff"},
                   "keyword1": {"value": f"{msg}", "color": "#173177"},
                   "keyword2": {"value": f"{time_lite}", "color": "#173177"},
                   "remark": {"value": "本内容由您通过睿视微闪api接口自行发送，点击【查看详情】进行查看，如果不是您本人进行的调用，请到 wxapi.rsws.top 进行重置！",
                              "color": "#8B0000"}
               }
               }
    )

    token1 = Token.query.order_by(Token.id.desc()).first()
    data = requests.post(
        f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token1}",
        json.JSONEncoder().encode(params))  # 推送消息请求
    errcode = data.text
    js = json.loads(errcode)
    print(js['errcode'])
    if js['errcode'] == 42001 or js['errcode'] == 41001 or js['errcode'] == 40001:
        print((js['errcode']))
        token()
        token1 = Token.query.order_by(Token.id.desc()).first()
        token1 = str(token1.token)
        data = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={token1}",
            json.JSONEncoder().encode(params))  # 推送消息请求
    add_msg = Message(title=title, msg=msg, uid=uid.id)
    db.session.add(add_msg)
    db.session.commit()

    return render_template('api.html', rswsid=rswsid)
    # return {"code":200,"data":{"title":title,"msg":msg},"message":"请求成功"}


@api.route('/msg/', methods=['POST', 'GET'])  # api发送页面
def blue_msg():
    title = request.args.get('title')
    msg = request.args.get('msg')
    return render_template('msg.html', title=title, msg=msg)


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

# @api.route('/logout', methods=['GET'])
# def logout():
#     session.pop('username', None)
#     return redirect('/')
