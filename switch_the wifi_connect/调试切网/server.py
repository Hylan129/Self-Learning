#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import subprocess

#创建socket套接字,并指定通信所用的协议
socket_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#重新使用IP地址和端口号
socket_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
#ip = socket.gethostbyname(socket.gethostname())
socket_server.bind(("10.7.5.105",8081))
socket_server.listen(5)

while True:
    print("等待客户端的连接.........")
    conn,address = socket_server.accept()
    print("链接已经生成")
    print("客户端的信息是:",address)

    """
    双方建立了连接后,就开始进行相同通信
    """
    while True:
        try:
            client_msg = conn.recv(1024).decode("utf-8")
            
            print("客户端发送的消息是:%s" %client_msg)
            res = subprocess.Popen(client_msg,shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            res_err = res.stderr.read()
            if res_err:
                cmd_res = res_err
            else:
                cmd_res = res.stdout.read()
            conn.send(cmd_res)

        except Exception:
            break

    conn.close()

socket_server.close()