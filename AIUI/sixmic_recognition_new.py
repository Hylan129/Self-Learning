#!/usr/bin/python
# coding=UTF-8

import serial,time,binascii
import gzip,csv,json

def port_open():
    ser.port = "COM1"       #设置端口号
    ser.baudrate = 115200   #设置波特率
    ser.bytesize = 8        #设置数据位
    ser.stopbits = 1        #设置停止位
    ser.parity = "N"        #设置校验位
    ser.open()              #打开串口,要找到对的串口号才会成功
    if(ser.isOpen()):
        print("AIUI串口连接成功！")
    else:
        print("串口打开失败")
 
def port_close():
    ser.close()
    if (ser.isOpen()):
        print("关闭失败")
    else:
        print("关闭成功")

def data_deal(receive):
    global text_voice,wakeup_angle
    if receive[0]==165 and receive[1]==1:
        global seqId
        seqId = ((receive[6] & 0xff) << 8) + (receive[5] & 0xff)
        send(buildConfirmPacket())
        
        DataLength = ((receive[4] & 0xff) << 8) + (receive[3] & 0xff) + 7
        receiveLength = len(receive)
        try:
            if receive[2] ==4:
                content = gzip.decompress(receive[7:DataLength]).decode()
            try:
                text_voice = json.loads(content)['content']['result']['intent']['text']
            except Exception as e:
                pass
            try:
                wakeup_angle = (json.loads(content)['content']['info']['angle'],json.loads(content)['content']['info']['CMScore'])
            except Exception as e:
                pass
                
            if(text_voice !=''):
                print(text_voice,wakeup_angle)
                text_voice =''
                
        except Exception as e:
            pass
        if  (DataLength +1) < receiveLength:
            return data_deal(receive[(DataLength +1):receiveLength])

def send(send_data):
    if (ser.isOpen()):
        ser.write(bytes.fromhex(send_data))
    else:
        print("发送失败")
def uft8tobytes(text):
    return text.encode()

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
    #print(list)
    checkCode_raw = 0;
    for i in range(len(list)):
        checkCode_raw = checkCode_raw + int(binascii.hexlify(list[i]),16);
    checkCode_end = bytes([(~checkCode_raw+1) & 0xff]);
    return checkCode_end;

if __name__ =='__main__':
    
    text_voice =''
    wakeup_angle = (0,0)
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
    number = 0
    port_open()
    try:
        for i in range(3):
            send(buildShakePacket())
    except Exception as e:
        with open('err.txt','a') as code:
            code.write(str(e)+'serial\n')
        
    while True:
        try:
            receive = ser.read_all()
            #print(receive)
            if receive != b'':
                data_deal(receive)
            time.sleep(0.5)
        except Exception as e:
            with open('err.txt','a') as code:
                code.write(str(e)+'receive\n')