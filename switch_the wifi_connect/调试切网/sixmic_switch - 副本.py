#!/usr/bin/python
# coding=UTF-8

import serial
import time
import datetime
import binascii

ser = serial.Serial()
seqId = 0;
SYNC_HEAD = 0xA5;
USER_ID = 0x01;
SHAKE_HAND_TYPE = 0x01;
WIFI_CONFIG_TYPE = 0x02;
AIUI_CONFIG_TYPE = 0x03;
AIUI_MESSAGE_TYPE = 0x04;
CONTROL_MESSAGE_TYPE = 0x05;
CUSTOM_DATA_TYPE = 0x2A;
CONFIRM_MESSAGE_TYPE = 0xff;

def port_open():
    ser.port = "COM1"       #设置端口号
    ser.baudrate = 115200   #设置波特率
    ser.bytesize = 8        #设置数据位
    ser.stopbits = 1        #设置停止位
    ser.parity = "N"        #设置校验位
    ser.open()              #打开串口,要找到对的串口号才会成功
    if(ser.isOpen()):
        print("串口连接成功！")
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
        time.sleep(0.5)
        ser.read_all()
        ser.write(bytes.fromhex(send_data))
        time.sleep(1)
        receive = ser.read_all()
        print("receive1",len(receive),receive)
        try:
            if(len(receive)>7):
            #if :
                global seqId
                #seqId = (int.from_bytes(receive[6],byteorder = 'big') & 0xff) << 8) + int.from_bytes(receive[5],byteorder = 'big')
                seqId = ((receive[6] & 0xff) << 8) + receive[5]
                print(seqId,type(seqId))
                send(buildConfirmPacket())
                #send(buildShakePacket())
                #print("receive",len(receive),receive[0],receive[1],receive[2],receive[3],receive[4],receive[5],receive[6],type(receive[6]))
    
        except Exception as e:
            with open('err.txt','a') as code:
                code.write(str(e)+'\n')

    else:
        print("发送失败")
def uft8tobytes(text):
    return text.encode()

def wifi_config(wifi_name,wifi_psw):
    
    ssid = uft8tobytes(wifi_name);
    password = uft8tobytes(wifi_psw);
    encrypt = 0x02;
    
    global seqId
    
    setSeqId(seqId + 1);
    
    length = len(ssid) + len(password) + 4;
    
    command_wifi = []
    
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([WIFI_CONFIG_TYPE]));
    
    command_wifi.append(bytes([(length & 0xff)]));
    command_wifi.append(bytes([(length >> 8) & 0xff]));
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8) & 0xff]));
    
    command_wifi.append(bytes([0x00]));
    command_wifi.append(bytes([encrypt]));
    command_wifi.append(bytes([len(ssid)]));
    command_wifi.append(bytes([len(password)]));

    for i in range(len(ssid)):
        command_wifi.append(bytes([ssid[i]]));
   

    for i in range(len(password)):
        command_wifi.append(bytes([password[i]]));
    
    check_code = checksum(command_wifi);
    command_wifi.append(check_code);
    
    return ''.join([binascii.hexlify(i).decode() for i in command_wifi]);

def buildShakePacket():
    command_wifi = [];
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([SHAKE_HAND_TYPE]));
    
    command_wifi.append(bytes([0x04]));
    command_wifi.append(bytes([0x00]));
    global seqId
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8 & 0xff)]));
    command_wifi.append(bytes([0xA5]));
    command_wifi.append(bytes([0x00]));
    command_wifi.append(bytes([0x00]));
    command_wifi.append(bytes([0x00]));
    
    check_code = checksum(command_wifi);
    command_wifi.append(check_code);
    return ''.join([binascii.hexlify(i).decode() for i in command_wifi]);

def buildConfirmPacket():
    command_wifi = [];
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([CONFIRM_MESSAGE_TYPE]));
    
    command_wifi.append(bytes([0x04]));
    command_wifi.append(bytes([0x00]));
    global seqId
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8 & 0xff)]));
    command_wifi.append(bytes([0xA5]));
    command_wifi.append(bytes([0x00]));
    command_wifi.append(bytes([0x00]));
    command_wifi.append(bytes([0x00]));
    
    check_code = checksum(command_wifi);
    command_wifi.append(check_code);
    return ''.join([binascii.hexlify(i).decode() for i in command_wifi]);

            
def setSeqId(id):
    global seqId
    seqId = id;
    
def checksum(list):
    print(list)
    checkCode_raw = 0;
    for i in range(len(list)):
        checkCode_raw = checkCode_raw + int(binascii.hexlify(list[i]),16);
    checkCode_end = bytes([(~checkCode_raw+1) & 0xff]);
    return checkCode_end;

if __name__ == '__main__':
    
    port_open()
    send(buildShakePacket())
    send(buildShakePacket())
    send(buildShakePacket())

    while(True):
        try:
            ssid = input('请输入网络账号名称：').strip()
            password = input('请输入网络账号密码：').strip()
            command_aiui = wifi_config(ssid,password)
            print(command_aiui)
            #print([binascii.hexlify(i).decode() for i in command_aiui])
            #print("send：",[int.from_bytes(i,byteorder = 'big') for i in command_aiui])
            send(command_aiui)
        except Exception as e:
            with open('err.txt','a') as code:
                code.write(str(e))
            port_close()
    



