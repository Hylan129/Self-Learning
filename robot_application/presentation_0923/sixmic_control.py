#!/usr/bin/python
# coding=UTF-8

import requests,json

old_information = ['','',False,False]
new_information = ['','',False,False]
voice_key = ''

def getsixmic_information():
    global old_information,new_information,update_information,voice_key
    #'yxp','m_IsAlarm'  'ycp','m_YCValue'
    if new_information[0] !='':old_information = new_information
    old_information[2] = new_information[2]
    try:
        login_message = requests.post('http://10.7.5.105:8088/GWService.asmx/LoginService',data ={'userName':'admin','userPwd':'admin' })
        if login_message.text[76:-9] == 'ADMIN':
            login_message.close()
            sixmic_message = requests.get('http://10.7.5.105:8088/GWService.asmx/GetRealTimeData',params = {'equip_no':6,'table_name':'ycp'})
            sixmic_text = json.loads(sixmic_message.text[76:-9])
            sixmic_message.close()
            sixmic_status = requests.get('http://10.7.5.105:8088/GWService.asmx/GetRealTimeData',params = {'equip_no':6,'table_name':'yxp'})
            sixmic_status_value = json.loads(sixmic_status.text[76:-9])
            sixmic_status.close()
            #返回内容：1、识别内容；2、识别角度；3、唤醒状态；4、联网状态
            new_information = [value['m_YCValue'] for value in sixmic_text[0:2]] + [value['m_IsAlarm'] for value in sixmic_status_value]
            if new_information[0] != old_information[0]: print(new_information)
            if new_information[0] == old_information[0]: new_information[0] = ''
            return new_information
    except Exception as e:
        with open('program_error.txt','a') as result:
                result.write("\n************"+ str(e) +'getsixmic_message\n')

def sixmic_speak(equip_no,set_no,strValue=''):
    #6,3机器人发声
    talk_parm = {"equip_no":equip_no,"setNo":set_no,"strValue":strValue}
    req_speak = requests.get("http://10.7.5.105:8088/GWService.asmx/SetupsCommand2?",params = talk_parm)
    req_speak.close()

def wake_or_sleep(equip_no,set_no):
    #6,2手动唤醒;6,8手动休眠
    wake_setting = {"equip_no":equip_no,"setNo":set_no}
    req_wake_or_sleep = requests.get("http://10.7.5.105:8088/GWService.asmx/SetupsCommand1?",params = wake_setting)
    req_wake_or_sleep.close()