#!/usr/bin/python
# coding=UTF-8

import serial,time

ser = serial.Serial()
humansensor_value = []


def port_open(com_port):
    ser.port = com_port       #设置端口号
    ser.baudrate = 9600   #设置波特率
    ser.bytesize = 8        #设置数据位
    ser.stopbits = 1        #设置停止位
    ser.parity = "N"        #设置校验位
    ser.open()              #打开串口,要找到对的串口号才会成功
    if(ser.isOpen()):
        print("人体感应器连接成功！！！")
    else:
        print("串口打开失败")
 
def port_close():
    ser.close()
    if (ser.isOpen()):
        print("关闭失败")
    else:
        print("关闭成功")

def send(send_data):

    if (ser.isOpen()):
        
        ser.write(bytes.fromhex(send_data)) #Hex发送
        
    else:
        print("发送失败")

def humansensor_status():
    global humansensor_value
    while(True):
        receive = str(ser.read_all().hex())
        humansensor_value.append(receive)