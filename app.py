from flask import Flask, render_template, session, jsonify
import time
import requests
import re

app = Flask(__name__)

app.secret_key = 'gsrgesgeg'


@app.route('/login')
def login():
    ctime = int(time.time() * 1000)
    qcodeurl = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}".format(ctime)

    resp = requests.get(qcodeurl)
    ret = re.findall('uuid = "(.*)";', resp.text)[0]
    session['qcode'] = ret
    return render_template('login.html',qcode=ret)

@app.route('/check_login')
def check_login():
    qcode = session['qcode']
    ctime = int(time.time() * 1000)
    check_login_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=1&r=-2040274130&_={1}'.format(qcode,ctime)
    resp = requests.get(check_login_url)
    result = {'code':408}
    if 'window.code=408;' in resp.text:
        return jsonify(result)

    elif 'window.code=201;' in resp.text:
        result['code'] = 201
        result['avatar'] = re.findall("window.userAvatar = '(.*)';",resp.text)[0]
        return jsonify(result)

    elif 'window.code=200;' in resp.text:
        result['code'] = 200
        print(resp.text)
        result['redirect_uri'] = re.findall('redirect_uri="(.*)";',resp.text)[0]
        return jsonify(result)

    return '检查是否已经登录'


@app.route('/index')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run()

