#!/usr/bin/python
# coding=UTF-8

import serial,time,binascii,json,gzip

ser = serial.Serial()
seqId = 0;
text_voice = ''
wakeup_angle = (0,0)
voice_number = 0

SYNC_HEAD = 0xA5;
USER_ID = 0x01;
SHAKE_HAND_TYPE = 0x01;
WIFI_CONFIG_TYPE = 0x02;
AIUI_CONFIG_TYPE = 0x03;
AIUI_MESSAGE_TYPE = 0x04;
CONTROL_MESSAGE_TYPE = 0x05;
CUSTOM_DATA_TYPE = 0x2A;
CONFIRM_MESSAGE_TYPE = 0xff;

START_TTS = "{\"type\": \"tts\",\"content\": {\"action\": \"start\",\"text\": \"******\"}}"
VOICE_CONTROL_MESSAGE = "{\"type\": \"voice\",\"content\": {\"enable_voice\":MYVOICE}}"
RESET_WAKE_MESSAGE = "{\"type\": \"aiui_msg\",\"content\": {\"msg_type\": MY_MSG_TYPE,\"arg1\": 0,\"arg2\": 0,\"params\": \"\"}}"

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
        try:
            ser.write(bytes.fromhex(send_data))
        except Exception as e:
            with open('err.txt','a') as code:
                code.write(str(e)+'\n')
    else:
        print("发送失败")

def receive_voice():
    while True :
        if (ser.isOpen()):
            receive_all = ser.read_all()
            try:
                data_deal(receive_all)
            except Exception as e:
                pass
            time.sleep(0.5)
        else:
            print("接收失败！")

def data_deal(receive):
    global text_voice,wakeup_angle,voice_number
    if receive != b'':
        voice_number += 1
    else:
        voice_number = 0
        
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
                
        except Exception as e:
            pass
        
        if  (DataLength +1) < receiveLength:
            return data_deal(receive[(DataLength +1):receiveLength])

def uft8tobytes(text):
    return text.encode()

def text_broadcast(text):
    
    text_confirm = START_TTS.replace("******", text)
    
    text_send = uft8tobytes(text_confirm)
    
    global seqId
    
    setSeqId(seqId + 1);
    
    length = len(text_send);
    
    command_wifi = []
    
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([CONTROL_MESSAGE_TYPE]));
    
    command_wifi.append(bytes([(length & 0xff)]));
    command_wifi.append(bytes([(length >> 8) & 0xff]));
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8) & 0xff]));

    for i in range(length):
        command_wifi.append(bytes([text_send[i]]));

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

def voice_status(value):

    if (value == 1):
        aiui_config_msg = VOICE_CONTROL_MESSAGE.replace("MYVOICE", "true")
    else:
        aiui_config_msg = VOICE_CONTROL_MESSAGE.replace("MYVOICE", "false")

    aiui_config_msg_send = uft8tobytes(aiui_config_msg);
    
    global seqId

    setSeqId(seqId + 1);
    
    length = len(aiui_config_msg_send);
    
    command_wifi = []
    
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([CONTROL_MESSAGE_TYPE]));
    
    command_wifi.append(bytes([(length & 0xff)]));
    command_wifi.append(bytes([(length >> 8) & 0xff]));
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8) & 0xff]));

    for i in range(length):
        command_wifi.append(bytes([aiui_config_msg_send[i]]));

    check_code = checksum(command_wifi);
    command_wifi.append(check_code);
    
    return ''.join([binascii.hexlify(i).decode() for i in command_wifi]);

def wakeup_status(value):

    if (value == 1):
        aiui_config_msg = RESET_WAKE_MESSAGE.replace("MY_MSG_TYPE", "8")
    else:
        aiui_config_msg = RESET_WAKE_MESSAGE.replace("MY_MSG_TYPE", "7")

    aiui_config_msg_send = uft8tobytes(aiui_config_msg);
    
    global seqId

    setSeqId(seqId + 1);
    
    length = len(aiui_config_msg_send);
    
    command_wifi = []
    
    command_wifi.append(bytes([SYNC_HEAD]));
    command_wifi.append(bytes([USER_ID]));
    command_wifi.append(bytes([CONTROL_MESSAGE_TYPE]));
    
    command_wifi.append(bytes([(length & 0xff)]));
    command_wifi.append(bytes([(length >> 8) & 0xff]));
    command_wifi.append(bytes([(seqId & 0xff)]));
    command_wifi.append(bytes([(seqId >> 8) & 0xff]));

    for i in range(length):
        command_wifi.append(bytes([aiui_config_msg_send[i]]));

    check_code = checksum(command_wifi);
    command_wifi.append(check_code);
    
    return ''.join([binascii.hexlify(i).decode() for i in command_wifi]);
    
def setSeqId(id):
    global seqId
    seqId = id;
    
def checksum(list):
    
    checkCode_raw = 0;
    for i in range(len(list)):
        checkCode_raw = checkCode_raw + int(binascii.hexlify(list[i]),16);
    checkCode_end = bytes([(~checkCode_raw+1) & 0xff]);
    return checkCode_end;
 