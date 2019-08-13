#!/usr/bin/python
# coding=UTF-8

import serial,time

ser = serial.Serial()

red  =  'AA07030000B4DD'
blue =  'AA07030001B5DD'
green = 'AA07030002B6DD'
human = 'aa07000100b2dd'

humansensor_value = ''


def port_open():
    ser.port = 'COM2'       #设置端口号
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
        humansensor_value = receive
        if receive != '':
            with open('log.txt','a') as status:
                status.write(receive + '\n')
def red_shanshuo():
    if (ser.isOpen()):
        for i in range(20):
            ser.write(bytes.fromhex(red)) #Hex发送
            time.sleep(0.1)
            ser.write(bytes.fromhex(green)) 
            time.sleep(0.1)
    else:
        print("发送失败")
    