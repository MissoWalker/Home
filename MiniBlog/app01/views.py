from django.shortcuts import render
import requests
from app01.untils import login_header
import re
try:
    from PIL import Image
except:
    pass
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"

def login(req):
    # su 是加密后的用户名
    username = req.POST.get("username")
    password = req.POST.get("password")
    su = login_header.get_su(username)
    sever_data = login_header.get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    showpin = sever_data["showpin"]
    password_secret = login_header.get_password(password, servertime, nonce, pubkey)

    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    if showpin == 0:
        login_page = session.post(login_url, data=postdata, headers=headers)
        login_page.encoding = "gbk"
    else:
        pcid = sever_data["pcid"]
        login_header.get_cha(pcid)
        postdata['door'] = input(u"请输入验证码")
        login_page = session.post(login_url, data=postdata, headers=headers)
    login_loop = (login_page.content.decode("GBK"))
    # print(login_loop)
    pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    loop_url = re.findall(pa, login_loop)[0]
    print(loop_url)
    # 此出还可以加上一个是否登录成功的判断，下次改进的时候写上
    login_index = session.get(loop_url, headers=headers)
    uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    # print(uuid)
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    # print(uuid_res)
    web_weibo_url = "http://weibo.com/u/%s/home?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    # weibo_page.encoding = "utf-8"
    html = weibo_page.text
    # print(html)
    ul = re.findall('<ul class=\\\\"user_atten clearfix W_f18\\\\">(.*)<\\\\/ul>',html)
    print(ul)
    attention_count = re.findall('follow\\\\">(\d+)<',ul[0])[0]
    fans_count = re.findall('fans\\\\">(\d+)<',ul[0])[0]
    article_count = re.findall('weibo\\\\">(\d+)<',ul[0])[0]
    agent_msg = {
        "attention_count":attention_count,
        "fans_count":fans_count,
        "article_count":article_count,
    }
    weibo_pa = r'<title>(.*?)</title>'
    # print(weibo_page.content.decode("utf-8"))
    userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    return render(req,"Login_Agent.html",agent_msg)
