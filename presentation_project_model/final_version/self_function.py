#!/usr/bin/env python
# coding=utf-8
import encodings.idna,time
import navigation_model,sixmic_control,constant

task_model = 0
wakeup_model = 0
task_status = 0

#巡航讲解主任务
def zjgg_presentation():
    global task_model,task_status
    while True:
        try:
            if(sixmic_control.text_voice =='开始参观' and task_model == 1):
                print('开始运动了哦！')
                sixmic_control.text_broadcast('开始运动！')
                xunhuan_wait = 1
                for go_point,text_point,time_point in zip(constant.position_list,constant.text_list,constant.time_list):
                    
                    navigation_model.navigation_position(go_point)
                    print('出发了！')
                    navigation_wait = 1
                    while navigation_wait:
                        if(navigation_model.navigation_value =='REACHED'):
                            print("coming!")
                            navigation_model.navigation_value =''
                            break
                        #if(navigation_model.navigation_value =='UNREACHED'):
                        #    navigation_model.navigation_position(go_point)
                        if (task_status == 1):
                            navigation_model.stop_motion()
                            while (True):
                                if (task_model == 0):
                                    navigation_wait = 0
                                    xunhuan_wait = 0
                                    break
                                if (task_status == 0):
                                    navigation_model.navigation_position(go_point)
                                    break
                                
                    if navigation_wait:
                        #sixmic_control.send(sixmic_control.wakeup_status(0))
                        #time.sleep(2)
                        sixmic_control.send(sixmic_control.text_broadcast(text_point))
                        time_wait = len(text_point)
                        
                        while time_wait:
                            time.sleep(0.3)
                            time_wait -= 1
                            if (task_status == 1):
                                while True:
                                    if (task_model == 0):
                                        time_wait = 0
                                        xunhuan_wait = 0
                                        break
                                    if (task_status == 0):
                                        sixmic_control.send(sixmic_control.text_broadcast(text_point))
                                        time_wait = len(text_point)
                                        break
                                    
                    if not (xunhuan_wait):
                        break
                    
        except Exception as e:
            with open('zjgg_err.txt','a') as code:
                code.write(str(e) + 'zjgg_presentation\n')
            
def motion_deal_status():
    
    if(navigation_model.navigation_value in ["HEADING","UNREACHABLE", "PLANNING"]):
        if (navigation_model.statuscode_value in (701,403)):
            sixmic_control.send(sixmic_control.text_broadcast('您好！请借过一下！'))
            time.sleep(5)

def voice_deal_status():
    global task_model,task_status
    
    if(sixmic_control.wakeup_angle !=(0,0) and task_model == 1):
        task_status = 1
        #sixmic_control.send(sixmic_control.wakeup_status(0))
        #sixmic_control.send(sixmic_control.voice_status(0))
        navigation_model.stop_motion()
        #sixmic_control.send(sixmic_control.voice_status(1))
        
        sixmic_control.send(sixmic_control.text_broadcast('我正在工作哦！'))
        sixmic_control.wakeup_angle =(0,0)
        
    if(sixmic_control.wakeup_angle !=(0,0) and task_model == 0):
        #sixmic_control.send(sixmic_control.wakeup_status(1))
        #sixmic_control.send(sixmic_control.voice_status(0))
        #navigation_model.stop_motion()
        #sixmic_control.send(sixmic_control.voice_status(1))
        sixmic_control.send(sixmic_control.text_broadcast('有什么需要帮忙的吗？'))
        sixmic_control.wakeup_angle =(0,0)
    if sixmic_control.text_voice =='开始参观' and task_model ==0:
        
        sixmic_control.send(sixmic_control.text_broadcast('讲解任务已开启！'))
        time.sleep(2)
        task_model = 1
        print('任务模式开启！')
        sixmic_control.send(sixmic_control.wakeup_status(1))
    elif sixmic_control.text_voice =='结束参观' and task_model == 1:
        sixmic_control.text_voice =''
        task_model = 0
        task_status = 0
        navigation_model.stop_motion()
        #sixmic_control.send(sixmic_control.voice_status(0))
        time.sleep(1)
        navigation_model.stop_motion()
        sixmic_control.send(sixmic_control.text_broadcast('任务已结束！'))
    elif (sixmic_control.text_voice == '继续参观') and task_model == 1 and task_status == 1:
        sixmic_control.text_voice =''
        sixmic_control.send(sixmic_control.text_broadcast('好的！那小派去忙去了哟！'))
        #sixmic_control.send(sixmic_control.voice_status(1))
        time.sleep(2)
        sixmic_control.send(sixmic_control.wakeup_status(1))
        task_status = 0
    else:
        if(sixmic_control.text_voice not in ['开始参观','结束参观','继续参观']) and sixmic_control.text_voice !='' and (task_model ==1):
            #sixmic_control.send(sixmic_control.voice_status(0))
            sixmic_control.text_voice =''
            print('静音成功！')
            #time.sleep(2)
            #sixmic_control.send(sixmic_control.voice_status(1))