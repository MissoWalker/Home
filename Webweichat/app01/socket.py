from django.shortcuts import HttpResponse

import socket


def send(req):
    get_str = 'GET %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\nAccept: */*\r\n\r\n'
    post_str = 'POST %s HTTP/1.1\r\nHost: %s\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36\r\n\r\n%s\r\n\r\n'
    a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a.connect(("www.sina.com.cn", 80))
    a.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    response = b''
    temp = a.recv(4096)
    while temp:
        temp = a.recv(4096)
        response += temp
    print(response)
    return HttpResponse(".........")
