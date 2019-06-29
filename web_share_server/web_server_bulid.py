#!/usr/bin/python
# -*- coding: UTF-8 -*-
import http.server
from socketserver import TCPServer
from socket import gethostbyname,gethostname
import os

def url_produce():
    ip = gethostbyname(gethostname())
    httpAddress = (ip, 8129)
    share_url = "http://%s:8129" %(ip)
    return share_url

def webserverbulid():
    Handler = http.server.SimpleHTTPRequestHandler
    ip = gethostbyname(gethostname())
    httpAddress = (ip, 8129)
    print("已开启WEB共享，共享文件夹路径：\n %s，\n\n共享链接地址：http://%s:8129 \n"%(os.getcwd(),ip))
    print("请扫描二维码或者输入链接地址到浏览器中打开，同局域网内手机、电脑均可链接共享！\n\n")
    print("将二维码照片或者链接地址分享他人即可！\n")
    os.system("请扫描二维码获取共享文件.png")
    with TCPServer(httpAddress, Handler) as httpd:
        httpd.serve_forever()