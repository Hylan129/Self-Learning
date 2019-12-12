import json,time,requests
from websocket import create_connection

navigation_value = ''
url = ['ws://10.7.5.88:8089/gs-robot/notice/navigation_status']
    
def status_navigtion_monitor():
    global navigation_value,url
    while True:
        try:
            ws_navigation = create_connection(url[0])
            print(ws_navigation)
            break
        except Exception as e:
            with open('motion_records.txt','a') as result_csv:
                result_csv.write(str(e) + 'status_navigtion_monitor\n')
        time.sleep(1)
    
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

def navigation_position(point):
    try:
        req_cd = requests.get('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=' + point)
        req_cd.close()
    except Exception as e:
        print(str(e))
    
def stop_motion():
    try:
        req = requests.get('http://10.7.5.88:8080/gs-robot/cmd/cancel_navigate')
        req.close()
    except Exception as e:
        print(str(e))