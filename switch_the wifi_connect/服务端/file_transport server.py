#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-21 下午8:04
# @Author  : LK
# @File    : server_socket_文件_服务端.py
# @Software: PyCharm

import socketserver
import struct

import os
import json
import struct


def sendRealFile(conn, filename):
    '''发送真是文件'''
    with open(filename, 'rb')as f:
        conn.sendall(f.read())

    print('发送成功')


def operafile(filename):
    '''对报头进行打包'''
    filesize_bytes = os.path.getsize(filename)
    head_dir = {
        'filename': 'new' + filename,
        'filesize_bytes': filesize_bytes,
    }
    head_info = json.dumps(head_dir)
    head_info_len = struct.pack('i', len(head_info))
    return head_info_len, head_info

class MyServer(socketserver.BaseRequestHandler):
    buffsize = 1024
    def handle(self):
        # self.request
        print('连接人的信息')
        print('conn是', self.request)  # conn
        print('addr是', self.client_address)  # addr

        while True:
            '''收发消息'''
            filename = input('请输入要发送的文件名加上后缀>>>').strip()
            #   判断文件是否存在

            head_info_len, head_info = operafile(filename)
            self.request.send(head_info_len)  # 这里是4个字节
            self.request.send(head_info.encode('utf-8'))  # 发送报头的内容
            sendRealFile(self.request, filename)


if __name__ == '__main__':
    # pass
    print('还没有人连接')
    s = socketserver.ThreadingTCPServer(('10.10.12.20', 8888), MyServer)  # 多线程
    #   服务器一直开着
    s.serve_forever()