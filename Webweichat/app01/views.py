from django.shortcuts import render, HttpResponse
import requests
import re
import json
import time


def ticket(html):
    from bs4 import BeautifulSoup
    ret = {}
    soup = BeautifulSoup(html, 'html.parser')
    print("<======================>")
    print(soup)
    for tag in soup.find(name='error').find_all():
        ret[tag.name] = tag.text
    return ret


def login(req):
    if req.method == "GET":
        uuid_time = time.time()
        base_uuid_url = "https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}"
        uuid_url = base_uuid_url.format(uuid_time)
        r1 = requests.get(uuid_url)
        # print(r1.text)
        result = re.findall('= "(.*)";', r1.text)
        uuid = result[0]

        req.session["UUID_TIME"] = uuid_time
        req.session["UUID"] = uuid
    return render(req, "Login.html", {"uuid": uuid})


def check_login(req):
    tip = req.GET.get('tip', 0)
    # print(11111111111111111)
    respone = {"code": 408, "data": None}
    # print(time.time())
    ctime = int(time.time() * 1000)
    # print(ctime)
    base_login_url = "https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip={1}&r=-755789912&_={2}"
    login_url = base_login_url.format(req.session["UUID"], tip, ctime)
    # print(login_url)
    r1 = requests.get(login_url)
    # print(r1.text)
    if "window.code=408" in r1.text:
        respone["code"] = 408
    elif "window.code=201" in r1.text:
        respone["code"] = 201
        # print(re.findall('window.userAvatar ="(.*)";',r1.text))
        respone["data"] = re.findall("window.userAvatar = '(.*)';", r1.text)[0]
    elif "window.code=200" in r1.text:
        req.session["LOGIN_COOKIES"] = r1.cookies.get_dict()
        # print("========================")
        # print(r1.text)
        base_redirect_url = re.findall('window.redirect_uri="(.*)";', r1.text)[0]
        redirect_url = base_redirect_url + "&fun=new&version=v2"

        # 获取凭证
        r2 = requests.get(redirect_url)
        print(r2.text)
        ticket_dict = ticket(r2.text)
        req.session["TICKED_DICT"] = ticket_dict
        req.session["TICKED_COOKIE"] = r2.cookies.get_dict()
        print(ticket_dict)
        # 初始化，获取最近联系人信息；公众号
        post_data = {
            "BaseRequest": {
                "DeviceID": "e384757757885382",
                'Sid': ticket_dict['wxsid'],
                'Uin': ticket_dict['wxuin'],
                'Skey': ticket_dict['skey'],
            }
        }
        print(post_data)
        init_url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-740036701&pass_ticket={0}".format(
            ticket_dict['pass_ticket'])
        r3 = requests.post(
            url=init_url,
            json=post_data
        )
        r3.encoding = 'utf-8'
        # print(r3.text)
        init_dict = json.dumps(r3.text)
        req.session["INIT_DICT"] = init_dict
        respone['code'] = 200

    return HttpResponse(json.dumps(respone))


def index(req):
    """
    显示最近联系人
    :param req: 
    :return: 
    """
    img_url = "https://wx.qq.com" + req.session['INIT_DICT']['User']['HeadImgUrl']
    res = requests.get(img_url, headers={'Referer': 'https://wx.qq.com/?&lang=zh_CN'})

    return render(req, 'index.html', {'img': res.content})
