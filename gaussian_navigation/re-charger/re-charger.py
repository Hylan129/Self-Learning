from urllib import request
import json,time,datetime

print('充电监控中.....')
#获取实时坐标，get请求
url1 = "http://10.7.5.88:8080/gs-robot/real_time_data/position"

#获取设备状态数据
url8 = "http://10.7.5.88:8080/gs-robot/data/device_status"

urls =[url1,url8]
i = 0
j = 1
m = 0
while(j):

    try:
        cd_position = request.Request('http://10.7.5.88:8080/gs-robot/data/positions?map_name=office')
        res_cd_position = request.urlopen(cd_position)
        content_cd_position = json.loads(res_cd_position.read().decode(encoding='utf-8'))

        for position in content_cd_position['data']:
            if(position['name']=='cd' and position['mapName']=='office' and int(position['type']) == 1):
                cd_x = position['gridX']
                cd_y = position['gridY']
                cd_r = position['angle']
                j = j - 1
        res_cd_position.close()
        #print(cd_x,cd_y,cd_r)
        #print(j)
        
        if(j == 1 ): time.sleep(60)
        
    except Exception as e:
    
        with open('program_error.txt','a') as result:
                
            result.write("\n************1" + '\n' + str(e) +'\n')

while(True):
    datas = []
    try:
        for url in urls:
            req = request.Request(url)
            res = request.urlopen(req)
            content = json.loads(res.read().decode(encoding='utf-8'))
            datas.append(content)
            res.close()
        data_row_1 = [
                    datas[0]["gridPosition"]["x"],datas[0]["gridPosition"]["y"],round(float(datas[0]["angle"]),2),
                    datas[1]["data"]["emergency"],datas[1]["data"]["battery"],datas[1]["data"]["batteryVoltage"],
                    datas[1]['data']['charger']
                    ]
        #print(str(i+1) +'：First\n',data_row_1) 
        datas = []
        
        time.sleep(60)
        
        for url in urls:
            req2 = request.Request(url)
            res2 = request.urlopen(req2)
            content = json.loads(res2.read().decode(encoding='utf-8'))
            datas.append(content)
            res2.close()
        data_row_2 = [
                    datas[0]["gridPosition"]["x"],datas[0]["gridPosition"]["y"],round(float(datas[0]["angle"]),2),
                    datas[1]["data"]["emergency"],datas[1]["data"]["battery"],datas[1]["data"]["batteryVoltage"],
                    datas[1]['data']['charger']
                    ]
                    
        
        #print(str(i+1) +'：Second\n',data_row_2)           
        datas = []
        
        difference_x = abs(float(data_row_2[0]) - float(data_row_1[0]))
        difference_y = abs(float(data_row_2[1]) - float(data_row_1[1]))
        difference_r = abs(float(data_row_2[2]) - float(data_row_1[2]))
        
        difference_x_cd = abs(float(data_row_2[0]) - float(cd_x))
        difference_y_cd = abs(float(data_row_2[1]) - float(cd_y))
        difference_r_cd = abs(float(data_row_2[2]) - float(cd_r))
        
        difference_b = float(data_row_2[4]) - float(data_row_1[4])
        difference_bv = float(data_row_2[5]) - float(data_row_1[5])
        
        
        if(difference_x <= 2 and difference_y <=2 and difference_r < 10 and 
            difference_x_cd <= 2 and difference_y_cd <=2 and difference_r_cd < 10 and 
            difference_b < 0 and difference_bv < 0 and
            data_row_2[3] == False and data_row_2[6] !=0 and data_row_2[6] !=4):
            
            #向前走60cm
            req_foreward = request.Request('http://10.7.5.88:8080/gs-robot/cmd/move_to?distance=0.3&speed=0.3')
            res_foreward = request.urlopen(req_foreward)
            
            #print('向前走60cm！')
            #print(res_foreward.read().decode(encoding='utf-8'))
            res_foreward.close()
            
            time.sleep(5)
            
            req_cd = request.Request('http://10.7.5.88:8080/gs-robot/cmd/position/navigate?map_name=office&position_name=cd')
            res_cd = request.urlopen(req_cd)
            
            #print('回去充电！')
            #print(res_cd.read().decode(encoding='utf-8'))
            res_cd.close()
            m = m + 1
            timenow = datetime.datetime.now().strftime('%Y-%m-%d ' ' %H:%M:%S')
            with open('re-charger.txt','a') as result:
                result.write(str(timenow) + '，断电回充：第' + str(m) + '次\n')
                
            time.sleep(120)
            
            req_stop = request.Request('http://10.7.5.88:8080/gs-robot/cmd/stop_current_task')
            res_stop = request.urlopen(req_stop)
            #print("stop 自动回充任务：",res_stop.read().decode(encoding='utf-8'))
            res_stop.close()
            
    except Exception as e:
    
        with open('program_error.txt','a') as result:
                
            result.write("\n************2" + '\n' + str(e) +'\n')
    i = i + 1