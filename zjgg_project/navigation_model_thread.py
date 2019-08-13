import json
from urllib import request
from websocket import create_connection

url = ['ws://10.7.5.88:8089/gs-robot/notice/device_status',
    'ws://10.7.5.88:8089/gs-robot/notice/status',
    'ws://10.7.5.88:8089/gs-robot/notice/system_health_status',
    'ws://10.7.5.88:8089/gs-robot/notice/navigation_status']

statuscode_value = 0
navigation_value = ''

def status_navigtion_monitor(url):
    global navigation_value
    while True:
        while True:  # 一直链接，直到连接上就退出循环
            try:
                ws = create_connection(url)
                break
            except Exception as e:
                print('连接异常1：', str(e))
                with open('connect_records.txt','a') as result_csv:
                    result_csv.write(str(e) + '1status_navigtion_monitor\n')
        while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
            try:
                response = ws.recv()
                status_feedback = json.loads(response)
                navigation_value = status_feedback['noticeType']
            except Exception as e:
                with open('getdata_records.txt','a') as result_csv:
                    result_csv.write(str(e) + '2status_navigtion_monitor\n')
                    
def status_status_monitor(url):
    global statuscode_value
    while True: 
        while True:  # 一直链接，直到连接上就退出循环
            try:
                ws = create_connection(url)
                break
            except Exception as e:
                print('连接异常2：', str(e))
                with open('connect_records.txt','a') as result_csv:
                    result_csv.write(str(e) + '1status_status_monitor\n')
                continue
        while True:  # 连接上，退出第一个循环之后，此循环用于一直获取数据
            try:
                response = ws.recv()
                status_feedback = json.loads(response)
                statuscode_value = status_feedback['statusCode']
            except Exception as e:
                with open('getdata_records.txt','a') as result_csv:
                    result_csv.write(str(e) + '2status_status_monitor\n')
        
def navigation_position(point):
    req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + point)
    res_cd = request.urlopen(req_cd)
    res_cd.close()



