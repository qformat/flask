# 微信发送模板信息

#### 介绍
使用flask构建的，通过登录，扫码关注公众号后，绑定ID，即可发送类似server酱一样的微信模板消息。

#### 软件架构
本源码是基于flask框架构建而成，

run.py是运行的主程序，整个项目的蓝图和基本设置都在这里可以找到。

models.py和exts.py是数据库架构程序

configs.py存放数据库链接端口

所有的功能文件都在runjob.views内
show.py是首页基础功能后台程序
user.py是注册登录基础功能后台程序
code.py是获取微信用户信息回调基础后台程序
api.py是在线调试发送模板信息基础后台程序

static文件夹内是所有css和js还有图片的存放地址

templates 文件夹内是包含所有html页面的存放地址
index.html是首页面
api.html是发送调试页
login.html是登录页
reg.html是注册页




#### 安装教程

1.  运行   pip install -r requirements.txt  ###进行环境安装
2.  安装完成后，打开configs.py 对数据库进行设置链接。
3.  运行 install_models.py进行数据库创建
4.  到这里基本上就完成了，运行run.py 就可以使用了
5.  有任何问题或者疑问可以加我QQ：52769804 进行询问，或者加微信：kge123666

#### 使用说明

API接口说明接口使用说明：
1.先关注微信公众号“睿视信息”，打开微信后扫描二维码后系统会自动为您分配专属的RswsID，注意不要透漏给别人。

2.如何调用：

（1）http://wxapi.rsws.top/apisend/?rswsid=专属rswsid&title=发送标题&msg=发送内容

（2）使用get或者post方式都可以进行调用，需要注意的是get方式有长度限制，而post方式没有长度限制，因此建议使用post方式来调用。

举例--使用python调用如下：

（1）直接使用requests.post或者request.get调用网址：

首先导入：import requests （导入模块）

直接使用命令：requests.post(http://wxapi.rsws.top/apisend/?rswsid=您获取到的(rswsid)&title=发送标题&msg=发送内容)

（2）使用调用变得通俗易懂更加直观的方式

import requests

rswsid = 'RSWS3dc817ce15311ecb491' # 这里替换成你专属的RswsID

ws_url = "http://wxapi.rsws.top/apisend/" # 接口地址

title = '要发送的标题' # 替换成想要发送的标题

msg = '要发送的内容' # 替换成想要发送的内容

ws_params = { # url链接参数

'rswsid': rswsid,

'title': title,

'msg': msg

}

resp = requests.post(ws_url,params=ws_params) # 使用post

if resp.status_code == 200:

    print('发送成功') # 判断是否发送成功

else:

    print('发送失败！')

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

####特别说明

本身开发这个api也是基于爱好和学习，有些地方做的不是很好，大家拿来看看参考一下就好，
有什么问题也可以私聊我进行探讨，感谢！

#### 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)
