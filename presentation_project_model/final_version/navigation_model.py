import json,time
from urllib import request
from websocket import create_connection

statuscode_value = 0
navigation_value = ''
url = ['ws://10.7.5.88:8089/gs-robot/notice/status',
    'ws://10.7.5.88:8089/gs-robot/notice/navigation_status']
    
def status_navigtion_monitor():
    global navigation_value,url
    while True:
        try:
            ws_navigation = create_connection(url[1])
            print(ws_navigation)
            break
        except Exception as e:
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + 'status_navigtion_monitor\n')
        time.sleep(2)
    
    while True:
        try:
            response_navigation = ws_navigation.recv()
            try:
                navigation_feedback = json.loads(response_navigation)
                navigation_value = navigation_feedback['noticeType']
            except Exception as e:
                pass
        except Exception as e:
            print(str(e))
                    
def status_status_monitor():
    global statuscode_value,url
    while True:
        try:
            ws_status = create_connection(url[0])
            print(ws_status)
            break
        except Exception as e:
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + 'status_status_monitor\n')
        time.sleep(2)
    while True:
        try:
            response_status = ws_status.recv()
            try:
                status_feedback = json.loads(response_status)
                statuscode_value = status_feedback['statusCode']
            except Exception as e:
                pass
        except Exception as e:
            print(str(e))
        
def status_monitor():
    global navigation_value,statuscode_value,url
    
    while True:
        try:
            ws_navigation = create_connection(url[1])
            #ws_status = create_connection(url[0])
            print(ws_navigation)
            #print(ws_status)
            #break
        except Exception as e:
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + 'status_navigtion_monitor\n')
    
        while True:
            try:
                
                response_navigation = ws_navigation.recv()
                try:
                    navigation_feedback = json.loads(response_navigation)
                    navigation_value = navigation_feedback['noticeType']
                except Exception as e:
                    pass
                
                """
                response_status = ws_status.recv()
                try:
                    status_feedback = json.loads(response_status)
                    statuscode_value = status_feedback['statusCode']
                except Exception as e:
                    pass
                """
            except Exception as e:
                print(str(e))
                if str(e) == 'Connection is already closed.':
                    while True:
                        try:
                            time.sleep(1)
                            ws_navigation = create_connection(url[1])
                            break
                        except Exception as e:
                            print(str(e))

def navigation_position(point):
    try:
        req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + point)
        res_cd = request.urlopen(req_cd)
        res_cd.close()
    except Exception as e:
        print(str(e))
    
def stop_motion():
    try:
        req = request.Request('http://10.7.5.88:8080/gs-robot/cmd/cancel_navigate')
        res = request.urlopen(req)
        res.close()
    except Exception as e:
        print(str(e))