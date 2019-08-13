# -*- coding: utf-8 -*-

from urllib import request
import human_sensor,threading,time,random
import configparser,json,navigation_model_thread
from urllib.parse import urlencode

def backcharger(position_go):
    req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + position_go)
    res_cd = request.urlopen(req_cd)
    res_cd.close()

def sixmic(equip_no,set_no,strValue=''):

    req_admin = request.Request(server_login)
    res_admin = request.urlopen(req_admin)
    res_admin.close()
    
    if strValue == '':
        talk_parm = {"equip_no":equip_no,"setNo":set_no}
        req_talk = request.Request(sixmic_use1 + urlencode(talk_parm))
        res_talk = request.urlopen(req_talk)
        res_talk.close()
    else:
        talk_parm = {"equip_no":equip_no,"setNo":set_no,"strValue":strValue}
        req_talk = request.Request(sixmic_use2 + urlencode(talk_parm))
        res_talk = request.urlopen(req_talk)
        res_talk.close()
    
def touch_feedback():
    number_count = []
    while True:
        #print("touch_feedback:",navigation_model_thread.statuscode_value[0])
        try:
            if navigation_model_thread.statuscode_value != []:
            
                value = navigation_model_thread.statuscode_value.pop(0)
                print(value)
                
                if value == 701 or value == 403:
                    human_sensor.send(green)
                    sixmic('6','3','有人来了哦！')
                else:
                    human_sensor.send(blue)
                    print(value)
                    
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************" + str(e) +'number\n')
                
if __name__ == '__main__':
    
    number = 0
    #'02':[['干啥','我在呢'],5],
    touch_msg = {
                '04':[['您好！请别摸我头上的角角'],5],
                '08':[['您好！请别摸我头上的角角'],5],
                '10':[['是带我去玩吗？'],5],
                '20':[['谁牵我的小手'],5],
                }
    red  =  'AA07030000B4DD'
    green =  'AA07030001B5DD'
    blue = 'AA07030002B6DD'
    human = 'aa07000100b2dd'
    config = configparser.ConfigParser()
    
    try:
        config.readfp(open(r'setting.ini'))
        ip = config.get("touch_setting","ip")
        position_nav = config.get("touch_setting","position")
    except Exception as e:
        with open('program_error.txt','a') as result:
            result.write("\n************" + str(e) +'setting.ini\n')
            
    if ip !='' and position_nav != '':
        server_login = 'http://' + ip + ':8088/GWService.asmx/LoginService?userName=admin&userPwd=admin'
        sixmic_use1 = "http://" + ip + ":8088/GWService.asmx/SetupsCommand1?"
        sixmic_use2 = "http://" + ip + ":8088/GWService.asmx/SetupsCommand2?"
        
        try:
            human_sensor.port_open()
            
            #t1 = threading.Thread(target = human_sensor.humansensor_status)
            t1 = threading.Thread(target = navigation_model_thread.status_status_monitor,args = (navigation_model_thread.url[1],))
            t2 = threading.Thread(target = touch_feedback)
            t1.start()
            t2.start()
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************"+ str(e) +'main\n')
    else :
        print('setting配置为空！')
        input('Enter To Exit！')