#!/usr/bin/python
# -*- coding: UTF-8 -*-
import qrcode_make
import web_server_bulid

if __name__ == '__main__':
    #建立web服务器
    share_url = web_server_bulid.url_produce()
    #生成二维码
    qrcode_make.qrcode_produce(share_url)
    web_server_bulid.webserverbulid()