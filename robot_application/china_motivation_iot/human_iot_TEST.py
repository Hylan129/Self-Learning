# -*- coding: utf-8 -*-

from urllib import request
import human_sensor,threading,time,random
import configparser,json
from urllib.parse import urlencode

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
    global number,number_set,voice,isposition
    number_count = []
    while True:
        try:
            if human_sensor.humansensor_value != []:
            
                value = human_sensor.humansensor_value.pop(0)
                touch_number = value[6:8]
                #print(type(isposition),value)
                if value[4:8] == '0001':
                    if number == 0 and isposition:
                        #print('我说话了哦！')
                        sixmic('6','3',voice.strip())
                    number += 1
                    if number >= int(number_set):
                        number = 0
                if value[4:8] == '0000':
                    number = 0
                if value[4:6] == '01':
                    if touch_number != '00':
                        human_sensor.send(red)
                    else:
                        human_sensor.send(blue)
                        
                    if(touch_number == '02'):
                        sixmic('6','2')
                        
                    if (touch_number in touch_msg) :
                        if touch_msg[touch_number][1]==5:
                            sixmic('6','3',random.choice(touch_msg[touch_number][0]))
                            number_count.append(touch_number)
                    if(number_count != []):
                        for x in number_count:
                            touch_msg[x][1] -= 1
                            if(touch_msg[x][1] <= 0):
                                touch_msg[x][1] = 5
                                number_count.remove(x)
                    
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************" + str(e) +'number\n')
def getrealposition():
    req_postion = request.Request("http://10.7.5.88:8080/gs-robot/real_time_data/position")
    req_postion_open = request.urlopen(req_postion)
    data = json.loads(bytes.decode(req_postion_open.read()))
    req_postion_open.close()
    return [data['angle'],data['gridPosition']['x'],data['gridPosition']['y']]

def isonposition():
    
    global isposition
    while True:
        try:
            real_position = getrealposition()
            isposition = abs(real_position[0] - int(target_postion[0])) <= 10 and abs(real_position[1] - int(target_postion[1])) <= 15 and abs(real_position[2] - int(target_postion[2])) <= 15
            #print(isposition)
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************" + str(e) +'isonposition\n')
            
if __name__ == '__main__':
    
    number = 0 
    isposition = False
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
        number_set = config.get("touch_setting","number")
        com_port = config.get("touch_setting","com_port")
        voice = config.get("touch_setting","voice")
        target_postion  = config.get("touch_setting","target_postion").split('#')
    except Exception as e:
        with open('program_error.txt','a') as result:
            result.write("\n************" + str(e) +'setting.ini\n')
            
    if ip !='' and number_set != '' and com_port != '' and voice != '':
        server_login = 'http://' + ip + ':8088/GWService.asmx/LoginService?userName=admin&userPwd=admin'
        sixmic_use1 = "http://" + ip + ":8088/GWService.asmx/SetupsCommand1?"
        sixmic_use2 = "http://" + ip + ":8088/GWService.asmx/SetupsCommand2?"
        
        try:
            human_sensor.port_open(com_port.strip())
            t1 = threading.Thread(target = human_sensor.humansensor_status)
            t2 = threading.Thread(target = touch_feedback)
            t3 = threading.Thread(target = isonposition)
            t1.start()
            t2.start()
            t3.start()
        except Exception as e:
            with open('program_error.txt','a') as result:
                result.write("\n************"+ str(e) +'main\n')
    else :
        print('setting配置为空！')
        input('Enter To Exit！')