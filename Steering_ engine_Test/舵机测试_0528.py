#!/usr/bin/python
# coding=UTF-8

import serial
import time
import datetime
import tkinter #导入tkinter模块
from tkinter import ttk
import serial.tools.list_ports
import binascii
import threading
import xlwt


root  = tkinter.Tk()
root.minsize(500,300)
root.maxsize(500,300)

root.title('舵机测试')

command1 = tkinter.StringVar()

command2 = tkinter.StringVar()

command3 = tkinter.StringVar()

command4 = tkinter.StringVar()


button0 = tkinter.Button(root,bg = 'white')
button0.place(x=248,y=0,width=4,height=300)

button1 = tkinter.Button(root,text='默认左右转动',command = lambda : start_test())
button1.place(x=40,y=20,width=85,height=40)

button2 = tkinter.Button(root,text='结束任务',command = lambda : port_close())
button2.place(x=135,y=20,width=85,height=40)

button3 = tkinter.Button(root,text='单指令运转',command = lambda : command_send1(command1.get()))
button3.place(x=40,y=70,width=175,height=40)

button3 = tkinter.Button(root,text='多指令运转',command = lambda : command_send2(command1.get(),command2.get(),command3.get()))
button3.place(x=40,y=110,width=175,height=40)

entry1 = tkinter.Entry(root,bg = 'white',textvariable = command1)
entry1.place(x = 300,y=10,width=199,height=30)

label1 = tkinter.Label(root,text="指令1")
label1.place(x=255,y=10)

entry2 = tkinter.Entry(root,textvariable = command2)
entry2.place(x = 300,y=42,width=199,height=30)

label2 = tkinter.Label(root,text="指令2")
label2.place(x=255,y=42)

entry3 = tkinter.Entry(root,textvariable = command3)
entry3.place(x = 300,y=72,width=199,height=30)

label3 = tkinter.Label(root,text="圈次")
label3.place(x=255,y=72)

entry4 = tkinter.Entry(root,textvariable = command4)
entry4.place(x = 300,y=102,width=199,height=30)

label4 = tkinter.Label(root,text="状态包")
label4.place(x=255,y=102)

'''
Text0 = tkinter.Label(root,text="1.转180度:\n FFFF0107031E00020002D2 \n 2.转到初始位置：\n FFFF0107031E0000FF03D4 \n 3.转到最大位移位置：\n FFFF0107031EFF03FF03D2",justify='left',bg='white')
Text0.place(x=255,y=150,width=245,height=150)
'''
label4=tkinter.Label(root,text="指令参考",font = ('微软雅黑',9),fg = 'red')
label4.place(x=255,y=150)

Choice= tkinter.StringVar()
Command_list = tkinter.StringVar()

lable_box = tkinter.Label(root,text="可用串口")
lable_box.place(x=36,y=177)

Box2 = ttk.Combobox(root,textvariable=Choice,state='readonly')
Box2['values']= list(serial.tools.list_ports.comports())
Box2.place(x=90,y=170,width =85,height=40)

Box3 = ttk.Combobox(root,state='readonly')
Box3['values']= ('1.转180度:FFFF0107031E00020002D2','2.转到0°位置：FFFF0107031E0000FF03D4','3.转到300°位置：FFFF0107031EFF03FF03D2','4.查询内部温度：FFFF0104022B01CC')
Box3.place(x=255,y=180,width=245,height=50)


ser = serial.Serial()

rorate_180='FFFF0107031E00020002D2'
rorate_0='FFFF0107031E0000FF03D4'
rorate_300='FFFF0107031EFF03FF03D2'
temp='FFFF0104022B01CC'
 
def port_open():

    if(Choice.get()!=''):
        ser.port = Choice.get().split()[0]       #设置端口号
        print(ser.port)
        ser.baudrate = 115200   #设置波特率
        ser.bytesize = 8        #设置数据位
        ser.stopbits = 1        #设置停止位
        ser.parity = "N"        #设置校验位
        ser.open()              #打开串口,要找到对的串口号才会成功
        if(ser.isOpen()):
            print("舵机样品测试，连续测试4天，请勿动！！！")
        else:
            print("串口打开失败")
    else:
        print("串口未选择，请先选择串口！")
 
def port_close():
    ser.close()
    if (ser.isOpen()):
        print("关闭失败")
    else:
        print("关闭成功")

def port_close2():
    
    number = tkinter.StringVar()
    newwindow=tkinter.Tk()
    input_text=tkinter.Entry(newwindow,textvariable=number)
    input_text.place(x=10,y=10,width=60,height=40)
    input_number=number.get()

    button0 = tkinter.Button(newwindow,text="确认",command=lambda:port_close())
    button0.place(x=100,y=10,width=30,height=40)
    
    if(input_number==0):
    
        ser.close()
        if (ser.isOpen()):
            print("关闭失败")
        else:
            print("关闭成功")

    
def send(send_data):
    if (ser.isOpen()):
        
        ser.write(bytes.fromhex(send_data)) #Hex发送
        """
        print("发送成功",send_data)

        receive=ser.read_all()
        print(receive)
        command4.set(binascii.b2a_hex(receive))
        """
    else:
        print("发送失败")

def command_send1(send_data):
    if (send_data == ''):
        print("指令为空，或者输入错误，请重新输入！")
    else:

        if (ser.isOpen()):
        
            ser.write(bytes.fromhex(send_data)) #Hex发送

            print("发送成功",send_data)

            receive=ser.read_all()
            print(receive)
            command4.set(binascii.b2a_hex(receive))

            port_close()
        else:

            port_open()
            ser.write(bytes.fromhex(send_data)) #Hex发送

            print("发送成功",send_data)

            receive=ser.read_all()
            print(receive)
            command4.set(binascii.b2a_hex(receive))

            port_close()
            
def command_send2(send_data1,send_data2,circle_time):
    if ((send_data1 == '') | (send_data2 =='')):
        print("指令为空，或者输入错误，请重新输入！")
    else:
        if (ser.isOpen()):

            for i in range(int(circle_time)+1):
                    
                ser.write(bytes.fromhex(send_data1)) #Hex发送
                time.sleep(3)
                ser.write(bytes.fromhex(send_data2)) #Hex发送
                time.sleep(3)
                receive=ser.read_all()
                print(receive)
                command4.set(binascii.b2a_hex(receive))


            port_close()

        else:
            port_open()
            for i in range(int(circle_time)):
                    
                ser.write(bytes.fromhex(send_data1)) #Hex发送
                time.sleep(3)
                ser.write(bytes.fromhex(send_data2)) #Hex发送
                time.sleep(3)

                receive=ser.read_all()
                print(receive)
                command4.set(binascii.b2a_hex(receive))


            port_close()
 
def start():
    port_open()
    if(ser.isOpen()):
        send(rorate_0)
        
        myWorkbook = xlwt.Workbook()
        mySheet = myWorkbook.add_sheet('temparture records')
        mySheet.col(1).width = 256 * 25
        mySheet.col(2).width = 256 * 15
        mySheet.col(3).width = 256 * 15
        mySheet.col(4).width = 256 * 15
        
        myStyle0 = xlwt.easyxf("font: height 300,name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;")
        myStyle_centre = xlwt.easyxf("align: wrap on, vert centre, horiz centre;")
        myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;', num_format_str='0.0%')

        mySheet.write_merge(0, 1,0,4,"舵机测试内部温度记录表",myStyle0)
        mySheet.write(2,0,"No.",myStyle_centre)
        mySheet.write(2,1,"记录时间",myStyle_centre)
        mySheet.write(2,2,"舵机反馈代码",myStyle_centre)
        mySheet.write(2,3,"舵机温度值",myStyle_centre)
        mySheet.write(2,4,"备注",myStyle_centre)
        
        for i in (2*j for j in range(30000)):
            
            send(rorate_300)
            time.sleep(2)
            ser.read_all()
            print("温度读取1：")
            send(temp)
            time.sleep(1)
            receive=ser.read_all()
            timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #temparture=receive.decode('utf-8', errors='ignore')
            feedback0 = binascii.b2a_hex(receive)
            feedback = receive.hex()
            try:
                temparture = int(receive.hex()[10:12],16)
            except:
                temparture = "no signal feedback ! 0"
            command4.set(str(temparture) +"度")
            print(temparture)
            
            mySheet.write(i+3,0,i+1,myStyle_centre)
            mySheet.write(i+3,1,timenow,myStyle_centre)
            mySheet.write(i+3,2,feedback,myStyle_centre)
            mySheet.write(i+3,3,temparture,myStyle_centre)
            
            send(rorate_0)
            time.sleep(2)
            ser.read_all()
            print("温度读取2：")
            send(temp)
            time.sleep(1)
            
            receive=ser.read_all()
            timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #temparture=receive.decode('utf-8', errors='ignore')
            feedback0 = binascii.b2a_hex(receive)
            feedback = receive.hex()
            try:
                temparture = int(receive.hex()[10:12],16)
            except:
                temparture = "no signal feedback ! 0"
            command4.set(str(temparture) +"度")
            print(temparture)
            
            mySheet.write(i+4,0,i+1,myStyle_centre)
            mySheet.write(i+4,1,timenow,myStyle_centre)
            mySheet.write(i+4,2,feedback,myStyle_centre)
            mySheet.write(i+4,3,temparture,myStyle_centre)
            
            myWorkbook.save('temparture records'+ '.xls') 
            
        port_close()


threads = []
t1 = threading.Thread(target=start)
threads.append(t1)
t2 = threading.Thread(target=port_close2)
threads.append(t2)

def start_test():
    for t in threads:
        t.setDaemon(True)
        t.start()
    

root.mainloop()

