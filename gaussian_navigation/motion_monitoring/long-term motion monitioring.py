from urllib import request
import json 
import datetime
import xlwt
import time
#import socket 

myWorkbook = xlwt.Workbook()
mySheet = myWorkbook.add_sheet('records')
mySheet.col(1).width = 256 * 25
mySheet.col(2).width = 256 * 15
mySheet.col(3).width = 256 * 15
mySheet.col(4).width = 256 * 15
mySheet.col(5).width = 256 * 15
mySheet.col(6).width = 256 * 15
mySheet.col(7).width = 256 * 15
mySheet.col(8).width = 256 * 15
mySheet.col(9).width = 256 * 15
mySheet.col(10).width = 256 * 15

myStyle0 = xlwt.easyxf("font: height 300,name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;")
myStyle_centre = xlwt.easyxf("align: wrap on, vert centre, horiz centre;")
mySheet.write_merge(0,1,0,10,"机器人巡航监控（实时坐标+运动速度）",myStyle0)
mySheet.write(2,0,"No.",myStyle_centre)
mySheet.write(2,1,"查询时间",myStyle_centre)
mySheet.write(2,2,"坐标X",myStyle_centre)
mySheet.write(2,3,"坐标Y",myStyle_centre)
mySheet.write(2,4,"角度R",myStyle_centre)
mySheet.write(2,5,"线速度X",myStyle_centre)
mySheet.write(2,6,"角速度Z",myStyle_centre)
mySheet.write(2,7,"运动停止与否",myStyle_centre)
mySheet.write(2,8,"急停按下与否",myStyle_centre)
mySheet.write(2,9,"剩余电量",myStyle_centre)
mySheet.write(2,10,"备注",myStyle_centre)
myWorkbook.save('Motion monitoring'+ '.xls')

#获取实时坐标，get请求
url1 = "http://10.7.5.88:8080/gs-robot/real_time_data/position"

#获取实时线速度
url5 = "http://10.7.5.88:8080/gs-robot/real_time_data/cmd_vel"

#获取设备状态数据
url8 = "http://10.7.5.88:8080/gs-robot/data/device_status"

urls =[url1,url5,url8]
datas = []
i = 0
print("监控进行中......")
print("间隔10s抓取一次数据......")

while(True):
    for url in urls:

        ##获取实时坐标url1，运动控制url2，get方式
        req = request.Request(url)
        res = request.urlopen(req)
        
        timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        content = json.loads(res.read().decode(encoding='utf-8'))
        datas.append(content)
        
        
    data_row = [i+1,timenow,datas[0]["gridPosition"]["x"],datas[0]["gridPosition"]["y"],round(float(datas[0]["angle"]),2),
                datas[1]["data"]["linear"]["x"],round(float(datas[1]["data"]["angular"]["z"]),4),
                datas[2]["data"]["detailedBrakerDown"],datas[2]["data"]["emergency"],datas[2]["data"]["battery"],
                ]
    mySheet.write(i+3,0,i+1,myStyle_centre)
    mySheet.write(i+3,1,timenow,myStyle_centre)
    mySheet.write(i+3,2,datas[0]["gridPosition"]["x"],myStyle_centre)
    mySheet.write(i+3,3,datas[0]["gridPosition"]["y"],myStyle_centre)
    mySheet.write(i+3,4,round(float(datas[0]["angle"]),2),myStyle_centre)
    mySheet.write(i+3,5,datas[1]["data"]["linear"]["x"],myStyle_centre)
    mySheet.write(i+3,6,round(float(datas[1]["data"]["angular"]["z"]),4),myStyle_centre)
    mySheet.write(i+3,7,datas[2]["data"]["detailedBrakerDown"],myStyle_centre)
    mySheet.write(i+3,8,datas[2]["data"]["emergency"],myStyle_centre)
    mySheet.write(i+3,9,datas[2]["data"]["battery"],myStyle_centre)
    
    if  (datas[1]["data"]["linear"]["x"]!=0) & datas[2]["data"]["detailedBrakerDown"]:
        mySheet.write(i+3,10,"停顿异常！",myStyle_centre)
    myWorkbook.save('Motion monitoring'+ '.xls')
    
    i = i +1
    datas =[]
    time.sleep(1)
    
    

with open('program_error.txt','a') as result:
                
    result.write("\n******"+str(timenow)+"******"+'\n'+''.join(need_content)+'\n')
            
with open('motion_and_charger_information_records.csv','a',newline='') as result_csv:
    write_csv = csv.writer(result_csv,dialect='excel')
    if head !=[]:
        write_csv.writerow(head)
        head = []
    write_csv.writerow([str(timenow),dict_content['SSID'],dict_content['BSSID'],dict_content['状态'],dict_content['信道'],dict_content['信号'],dict_content['接收速率(Mbps)'],dict_content['传输速率 (Mbps)']])