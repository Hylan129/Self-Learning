from urllib import request
import json,csv
import datetime,time
import socket

#获取实时坐标，get请求
url1 = "http://10.7.5.88:8080/gs-robot/real_time_data/position"

#获取实时线速度
url5 = "http://10.7.5.88:8080/gs-robot/real_time_data/cmd_vel"

#获取设备状态数据
url8 = "http://10.7.5.88:8080/gs-robot/data/device_status"

urls =[url1,url5,url8]
datas = []
i = 0

head = ['No.','日期','时间','坐标X','坐标Y','角度R','线速度','角速度','运动速度','运动停止与否','急停按下与否','充电状态','电池电量','电池电压','主机名称','IP_information']

print('......\n')

while(True):

    try:
    
        timenow_1,timenow_2 = datetime.datetime.now().strftime('%Y-%m-%d'),datetime.datetime.now().strftime('%H:%M:%S')
        
        for url in urls:
            req = request.Request(url)
            res = request.urlopen(req)
            content = json.loads(res.read().decode(encoding='utf-8'))
            datas.append(content)

        ip_information = socket.gethostbyname_ex(socket.gethostname())
        data_row = [
                    i+1,timenow_1,timenow_2,
                    datas[0]["gridPosition"]["x"],datas[0]["gridPosition"]["y"],round(float(datas[0]["angle"]),2),
                    datas[1]["data"]["linear"]["x"],round(float(datas[1]["data"]["angular"]["z"]),4),
                    datas[2]["data"]["speed"],datas[2]["data"]["detailedBrakerDown"],datas[2]["data"]["emergency"],datas[2]["data"]["charger"],datas[2]["data"]["battery"],datas[2]["data"]["batteryVoltage"],
                    ip_information[0],'|'.join(ip_information[2])
                    ]
        with open('motion_and_charger_information_records.csv','a',newline='') as result_csv:
            write_csv = csv.writer(result_csv,dialect='excel')
            if head !=[]:
                write_csv.writerow(head)
                head = []
            write_csv.writerow(data_row)
    except Exception as e:
    
        with open('program_error.txt','a') as result:
                
            result.write("\n******"+str(timenow_1)+ ' ' + str(timenow_2) + "******" + '\n' + str(e) +'\n')
    
    i = i +1
    datas =[]
    time.sleep(2)