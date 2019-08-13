# -*- coding: utf-8 -*-

from urllib import request
import human_sensor,threading,time,random
import configparser,json
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
        #print(sixmic_use + urlencode(talk_parm))
        req_talk = request.Request(sixmic_use2 + urlencode(talk_parm))
        res_talk = request.urlopen(req_talk)
        res_talk.close()
    
def touch_feedback():
    number_count_02 = number_count_04 = number_count_08 = number_count_10 = number_count_20 = 3
    
    number_count = [number_count_02,number_count_04,number_count_08,number_count_10,number_count_20]
    while True:
        try:
            if human_sensor.humansensor_value != []:
            
                value = human_sensor.humansensor_value.pop(0)
                touch_number = value[6:8]
                
                if value[4:6] == '01':
                    if touch_number != '00':
                        human_sensor.send(red)
                    else:
                        human_sensor.send(blue)
                        
                    if(touch_number == '02'):
                        sixmic('6','2')
                        print('唤醒成功！')
                        
                    if(touch_number in ['08','0C','04']):
                        number += 1
                        print(number)
                        if number > 10:
                            backcharger(position_nav)
                            print('我去%s点了哦！'%  position_nav)
                            number = 0
                    else:
                        number = 0
                    if (touch_number in touch_msg):
                        sixmic('6','3',random.choice(touch_msg[touch_number]))
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************" + str(e) +'number\n')
if __name__ == '__main__':
    
    number = 0
    touch_msg = {'02':['干啥','我在呢'],
                '04':['您好！请别摸我头上的角角'],
                '08':['您好！请别摸我头上的角角'],
                '10':['是带我去玩吗？'],
                '20':['谁牵我的小手'],
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
            t1 = threading.Thread(target = human_sensor.humansensor_status)
            t2 = threading.Thread(target = touch_feedback)
            t1.start()
            t2.start()
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************"+ str(e) +'main\n')
    else :
        print('setting配置为空！')
        input('Enter To Exit！')