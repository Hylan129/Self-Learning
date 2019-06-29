#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-5-21 下午8:32
# @Author  : LK
# @File    : server_socket_文件客户端.py
# @Software: PyCharm
from socket import *
import os
import sys
import json
import struct

tcp_client = socket(AF_INET, SOCK_STREAM)
ip_port = (('10.10.12.20', 8888))
buffsize = 1024
tcp_client.connect_ex(ip_port)
print('等待服务端发送信息')


def recv_file(head_dir, tcp_client):
    filename = head_dir['filename']
    filesize_b = head_dir['filesize_bytes']
    recv_len = 0
    recv_mesg = b''
    f = open(filename, 'wb')
    while recv_len < filesize_b:
        if filesize_b - recv_len > buffsize:
            recv_mesg = tcp_client.recv(buffsize)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)
        else:
            recv_mesg = tcp_client.recv(filesize_b - recv_len)
            recv_len += len(recv_mesg)
            f.write(recv_mesg)

    f.close()
    print('文件传输完成')

while True:
    '''收发循环'''
    struct_len = tcp_client.recv(4)  #  接受报头的长度
    struct_info_len = struct.unpack('i',struct_len)[0]  #   解析得到报头信息的长度
    head_info = tcp_client.recv(struct_info_len)   #    接受报头的内容
    head_dir = json.loads(head_info.decode('utf-8'))              #   将报头的内容反序列化
    # #   文件信息
    # filename = head_dir['filename']
    # filesize = head_dir['filesize_bytes']
    recv_file(head_dir, tcp_client)