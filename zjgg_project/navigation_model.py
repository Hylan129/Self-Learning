import time,csv,threading,json
from urllib import request
from multiprocessing import Process
from websocket import create_connection
import sixmic_control

url = ['ws://10.7.5.88:8089/gs-robot/notice/device_status',
    'ws://10.7.5.88:8089/gs-robot/notice/status',
    'ws://10.7.5.88:8089/gs-robot/notice/system_health_status',
    'ws://10.7.5.88:8089/gs-robot/notice/navigation_status']
head = []
i = 0 
def status_feedback(url_init):
    def_name = url_init.split('/')[-1]
    while True:  # 一直链接，直到连接上就退出循环
        time.sleep(2)
        try:
            ws = create_connection(url_init)
            print(ws)
            break
        except Exception as e:
            print('连接异常：', e)
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + '\n')
            continue
    while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
        global i
        response = ws.recv()
        print(response)
        with open('motion_records.csv','a',newline='') as result_csv:
            write_csv = csv.writer(result_csv,dialect='excel')
            write_csv.writerow([i+1,def_name,response])
            i += 1
def status_navigtion_monitor():
    while True:  # 一直链接，直到连接上就退出循环
        try:
            ws = create_connection(url[3])
            break
        except Exception as e:
            print('连接异常：', e)
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + '\n')
            continue
    while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
        
        response = ws.recv()
        #print(response)
        status_feedback = json.loads(response)
        if status_feedback['noticeType'] == 'REACHED':
            ws.close()
            break
def status_status_monitor():
    while True:  # 一直链接，直到连接上就退出循环
        try:
            ws = create_connection(url[1])
            break
        except Exception as e:
            print('连接异常：', e)
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + '\n')
            continue
    while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
        
        response = ws.recv()
        #print(response)
        status_feedback = json.loads(response)
        if status_feedback['statusCode'] == 701:
            sixmic_control.send(sixmic_control.text_broadcast("大哥你好，借过一下！"))
            time.sleep(4)
            ws.recv()
            #break            
def navigation_position(point):
    req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + point)
    res_cd = request.urlopen(req_cd)
    res_cd.close()



