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
            if(sixmic_control.new_information[0] =='开始参观' and task_model == 1):
                print('开始运动了哦！')
                xunhuan_wait = 1
                while xunhuan_wait:
                    for go_point,text_point,time_point in list(zip(constant.position_list,constant.text_list,constant.time_list))[0:3]:
                        point_cicle = 1
                        print('出发了！')
                        while point_cicle:
                            sixmic_control.sixmic_speak(1,int(go_point))
                            navigation_wait = 1
                            while True :
                                if(navigation_model.navigation_value =='REACHED'):
                                    print("coming!")
                                    navigation_model.navigation_value =''
                                    sixmic_control.wake_or_sleep(6,8)
                                    break
                                
                                if (task_status == 1):
                                    navigation_model.stop_motion()
                                    while (True):
                                        if (task_model == 0):
                                            navigation_wait = 0 
                                            xunhuan_wait = 0 
                                            point_cicle = 0
                                            break
                                        if (task_status == 0 and task_model == 1 ):
                                            sixmic_control.sixmic_speak(1,int(go_point))
                                            break
                            if navigation_wait:
                                sixmic_control.sixmic_speak(6,3,text_point)
                                time_wait = len(text_point)
                                
                                while time_wait:
                                    time.sleep(0.3)
                                    time_wait -= 1
                                    if (task_status == 1):
                                        while True:
                                            if (task_model == 0):
                                                time_wait = 0 
                                                xunhuan_wait = 0 
                                                point_cicle = 0
                                                break
                                            if (task_status == 0 and task_model == 1 ):
                                                time_wait = ''
                                                break
                                if time_wait == 0: point_cicle = 0 
                        if not (xunhuan_wait):
                            break
        except Exception as e:
            with open('zjgg_err.txt','a') as code:
                code.write(str(e) + 'zjgg_presentation\n')

def voice_deal_status():
    global task_model,task_status
    sixmic_control.getsixmic_information()
    sixmic_status = (sixmic_control.new_information[2]== True and sixmic_control.old_information[2] ==False ) 
    if( sixmic_status and task_model == 1):
        task_status = 1
        navigation_model.stop_motion()
        sixmic_control.sixmic_speak(6,3,'我正在工作哦！')
    if( sixmic_status and task_model == 0):
        sixmic_control.sixmic_speak(6,3,'有什么需要帮忙的吗？')
        
    if sixmic_control.new_information[0] =='开始参观' and task_model ==0:
        
        sixmic_control.sixmic_speak(6,3,'讲解任务已开启！')
        task_model = 1
        print('任务模式开启！')
        time.sleep(2)
        sixmic_control.wake_or_sleep(6,8)
        #sixmic_control.old_information = sixmic_control.new_information
        
    elif sixmic_control.new_information[0] =='结束参观' and task_model == 1:
        task_model = 0
        task_status = 0
        navigation_model.stop_motion()
        sixmic_control.sixmic_speak(6,3,'任务已结束！')
        
    elif (sixmic_control.new_information[0] == '继续参观') and task_model == 1 and task_status == 1:
        #sixmic_control.old_information = sixmic_control.new_information
        sixmic_control.sixmic_speak(6,3,'好的！那小派去忙去了哟！')
        time.sleep(2)
        sixmic_control.wake_or_sleep(6,8)
        task_status = 0
    time.sleep(0.5)