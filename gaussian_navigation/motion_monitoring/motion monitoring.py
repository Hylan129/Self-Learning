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

#定距离定速度移动控制,get请求

url2 = "http://10.7.5.88:8080/gs-robot/cmd/move_to?distance=0.5&speed=0.3"

#是否结束定距离定速度移动任务，get请求

url3= "http://10.7.5.88:8080/gs-robot/cmd/is_move_to_finished"

#旋转，post请求

url4 = "http://10.7.5.88:8080/gs-robot/cmd/rotate"

request_rotate ={"rotateAngle":30,"rotateSpeed":0.3}

text_rotate = json.dumps(request_rotate).encode(encoding='utf-8')

#获取实时线速度
url5 = "http://10.7.5.88:8080/gs-robot/real_time_data/cmd_vel"

#获取设备状态数据

url8 = "http://10.7.5.88:8080/gs-robot/data/device_status"

#导航状态推送(web-socket)
url6 = "/gs-robot/notice/navigation_status port:8089"
#指示类设备状态(web-socket)
url7 = "/gs-robot/notice/device_status port:8089"

urls =[url1,url5,url8]
datas = []
i = 0
print("监控进行中......")
print("间隔1s抓取一次数据......")

while(True):
    for url in urls:

        ##获取实时坐标url1，运动控制url2，get方式
        req = request.Request(url)
    
        ##旋转控制，post方式
        #req = request.Request(url=url4,data=text_rotate)
        res = request.urlopen(req)
        timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        content = json.loads(res.read().decode(encoding='utf-8'))
        datas.append(content)

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