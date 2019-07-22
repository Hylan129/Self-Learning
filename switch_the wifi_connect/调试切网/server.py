#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import subprocess

import computer_switch
import sixmic_switch

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
    print("链接已经生成！客户端的信息是:",address)
    print("1-->切换主板网络，5-->刷新服务，6-->切换六麦网络！")

    """
    双方建立了连接后,就开始进行相同通信
    """
    while True:
        try:
            client_msg = conn.recv(1024).decode("gb2312",'replace').strip().split(',')
            print(client_msg)
            
            if(client_msg[0].strip()=='1' and len(client_msg)==3):
                feedback = computer_switch.wifi_switch(client_msg[1].strip(),client_msg[2].strip())
                conn.send(feedback.encode("gb2312",'replace'))
            elif (client_msg[0].strip()=='6' and len(client_msg)==3):
                feedback = sixmic_switch.wifi_switch(client_msg[1].strip(),client_msg[2].strip()) 
                conn.send(feedback.encode("gb2312",'replace'))
            elif (client_msg[0].strip()=='5' and len(client_msg)==1):
                feedback = sixmic_switch.kill_server()
                conn.send(feedback.encode("gb2312",'replace'))
            else:
                feedback = "输入错误，请重新输入！1-->切换主板网络，5-->刷新服务，6-->切换六麦网络！"
                conn.send(feedback.encode("gb2312",'replace'))

        except Exception as e:
            with open('err.txt','a') as code:
                code.write("server:"+str(e)+'\n')
            break

    conn.close()

socket_server.close()