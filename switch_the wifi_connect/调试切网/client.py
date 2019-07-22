#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket
import tkinter #导入tkinter模块
import tkinter.messagebox
import tkinter.filedialog
from tkinter import *

root  = tkinter.Tk()
root.minsize(500,300)
root.maxsize(500,300)

root.title("小π网络切换工具V01")

#SSID_INIT = PWD_INIT = ''
command_SSID = tkinter.StringVar()
command_PWD = tkinter.StringVar()
    
button1 = tkinter.Button(root,text='刷新服务',command = lambda : send_command_update('5'))
button1.place(x=40,y=20,width=85,height=40)

button2 = tkinter.Button(root,text='切换主板网络',command = lambda : msg_input('1'))
button2.place(x=135,y=20,width=85,height=40)

button2 = tkinter.Button(root,text='切换六麦网络',command = lambda : msg_input('6'))
button2.place(x=225,y=20,width=85,height=40)

def send_command_update(msg):

    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        socket_client.connect(("10.7.5.105",8081))
        socket_client.send(msg.encode("utf-8"))
    except:
        tkinter.messagebox.showerror('错误', '请连接导航盒WIFI后再试！')

    #server_msg = socket_client.recv(1024)
    server_msg = socket_client.recv(2048).decode("gb2312",'replace')
    print("服务端发送过来的数据是:%s"%server_msg)
    socket_client.close()
    tkinter.messagebox.showinfo('提示',server_msg)

def msg_input(number):
    
    msg_in = Toplevel(root)
    msg_in.minsize(300,200)
    msg_in.maxsize(300,200)
    
    msg_in.title("请输入网络账号密码")
    
    def setting():
        SSID_INIT = command_SSID.get()
        #print("SSID_INIT:"+ SSID_INIT)
        PWD_INIT = command_PWD.get()
        #print("PWD_INIT:"+ PWD_INIT)
        msg_in.destroy()
        send_command_update_2(number,SSID_INIT.strip(),PWD_INIT.strip())
        
    label1 = tkinter.Label(msg_in,text="SSID")
    label1.place(x=10,y=42,width=100)

    entry1 = tkinter.Entry(msg_in,textvariable = command_SSID)
    entry1.place(x = 100,y=42,width=180,height=30)
    
    label2 = tkinter.Label(msg_in,text="PASSWORD")
    label2.place(x=10,y=92,width=100)

    entry2 = tkinter.Entry(msg_in,textvariable = command_PWD)
    entry2.place(x = 100,y=92,width=180,height=30)
    
    button0 = tkinter.Button(msg_in,text="提交",command=lambda: setting())
    button0.place(x=120,y=140)
    
    
def send_command_update_2(number,ssid,pwd):
    socket_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        socket_client.connect(("10.7.5.105",8081))
    except:
        tkinter.messagebox.showerror('错误', '请连接导航盒WIFI后再试！')
    
    socket_client.send((number+','+ssid+','+pwd).encode("utf-8"))

    #server_msg = socket_client.recv(1024)
    server_msg = socket_client.recv(2048).decode("gb2312",'replace')
    print("服务端发送过来的数据是:%s"%server_msg)
    socket_client.close()
    tkinter.messagebox.showinfo('提示',server_msg)
root.mainloop()

