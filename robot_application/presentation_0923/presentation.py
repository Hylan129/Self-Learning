#!/usr/bin/env python
# coding=utf-8
import time,threading,self_function
import encodings.idna,sixmic_control,navigation_model

def get_status_information():
    while True:
        try:
            #运动导航状态信息监控
            navigation_model.status_navigtion_monitor()
            navigation_model.status_status_monitor()
        except Exception as e :
            with open('zjgg_err.txt','a') as code:
                code.write(str(e) + 'get_status_information \n')
        
def deal_status():
    while True:
        try:
            #语音信息处理
            self_function.voice_deal_status()
            #运动信息处理
            #self_function.motion_deal_status()
        except Exception as e :
            with open('zjgg_err.txt','a') as code:
                code.write(str(e) + 'deal_status \n')

if __name__ == '__main__':
    try:
        print("开始运行了！")
        t1 = threading.Thread(target = navigation_model.status_navigtion_monitor)
        t2 = threading.Thread(target = deal_status)
        t3 = threading.Thread(target = self_function.zjgg_presentation)
        
        Threads = [t1,t2,t3]
        for t in Threads:
            t.start()
        
    except Exception as e:
        with open('zjgg_err.txt','a') as code:
            code.write(str(e) + 'zjgg_err \n')