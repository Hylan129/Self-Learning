import json
from urllib import request
from websocket import create_connection

url = ['ws://10.7.5.88:8089/gs-robot/notice/status',
    'ws://10.7.5.88:8089/gs-robot/notice/navigation_status']

statuscode_value = 0
navigation_value = ''

def status_navigtion_monitor():
    global navigation_value,url
        
    try:
        response_navigation = ws_navigation.recv()
        navigation_feedback = json.loads(response_navigation)
        navigation_value = navigation_feedback['noticeType']
    except Exception as e:
        try:
            ws_navigation = create_connection(url[1],timeout =2)
            print('nav连接成功！')
        except Exception as e:
            with open('zjgg_err.txt','a') as result_csv:
                result_csv.write(str(e) + '1status_navigtion_monitor\n')
                    
def status_status_monitor():
    global statuscode_value,url
        
    try:
        response_status = ws_status.recv()
        status_feedback = json.loads(response_status)
        statuscode_value = status_feedback['statusCode']
    except Exception as e:
        try:
            ws_status = create_connection(url[0],timeout =2)
            print('status连接成功！')
        except Exception as e:
            with open('zjgg_err.txt','a') as result_csv:
                result_csv.write(str(e) + '1status_status_monitor\n')
        
def navigation_position(point):
    req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + point)
    res_cd = request.urlopen(req_cd)
    res_cd.close()
    
def stop_motion():
    req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/cancel_navigate')
    res_cd = request.urlopen(req_cd)
    res_cd.close()