#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket

#1、创建一个socket套接字对象,同时需要指定网络通信所用的协议,在这里用的是TCP协议
socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#2、通过socket这个套接字向服务端发送链接请求
socket_client.connect(("127.0.0.1",8081))

"""
从下面开始双方将会基于这个链接进行相互通信
"""
while True:
    msg = input(">>:").strip()
    if not msg: continue
    socket_client.send(msg.encode("utf-8"))

    #server_msg = socket_client.recv(1024)
    server_msg = socket_client.recv(2048).decode("gb2312",'replace')
    print("服务端发送过来的数据是:%s"%server_msg)


socket_client.close()