#！/usr/bin/env python

#-*-coding:utf-8-*-

# 打开摄像头并灰度化显示
import cv2
import time
import similarity
import os
import datetime
import xlwt

myWorkbook = xlwt.Workbook()
mySheet = myWorkbook.add_sheet('temparture records')
mySheet.col(1).width = 256 * 25
mySheet.col(2).width = 256 * 15
mySheet.col(3).width = 256 * 15
mySheet.col(4).width = 256 * 15
mySheet.col(5).width = 256 * 15

myStyle0 = xlwt.easyxf("font: height 300,name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;")
myStyle_centre = xlwt.easyxf("align: wrap on, vert centre, horiz centre;")
myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on;align: wrap on, vert centre, horiz centre;', num_format_str='0.00%')

mySheet.write_merge(0,1,0,5,"机器人行走过程中疑似卡顿分析记录表",myStyle0)
mySheet.write(2,0,"No.",myStyle_centre)
mySheet.write(2,1,"疑似卡顿时间1",myStyle_centre)
mySheet.write(2,2,"疑似卡顿时间2",myStyle_centre)
mySheet.write(2,3,"拍照次数",myStyle_centre)
mySheet.write(2,4,"照片相似度",myStyle_centre)
mySheet.write(2,5,"备注",myStyle_centre)


capture = cv2.VideoCapture(0)
i=0

while(True):
    # 获取一帧
    if(i<5):
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('hylan', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('hylan', gray)
        cv2.waitKey(1)
        cv2.imwrite(".//lib_picture//" + str(i)+'.jpeg',frame)
        i=i+1
        time.sleep(0.1)
    else:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.namedWindow('hylan', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('hylan', gray)
        cv2.waitKey(1)
        cv2.imwrite(".//lib_picture//" + str(i)+'.jpeg',frame)
        timenow1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timenow2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        
        #当前照片与前5张照片对比，判断相似度
        
        new_picture=similarity.getImgHash(".//lib_picture//" + str(i)+'.jpeg')
        
        old_picture = similarity.getImgHash(".//lib_picture//" + str(i-1)+'.jpeg')
        
        similarity_value=similarity.getMH(new_picture,old_picture)
        
        print(str(i) + u"相似度" + str(similarity_value))
        
        #os.remove(".//lib_picture//" + str(i-5)+'.jpeg')
        
        #记录数据
        
        mySheet.write(i-5+3,0,i-5+1,myStyle_centre)
        mySheet.write(i-5+3,1,timenow1,myStyle_centre)
        mySheet.write(i-5+3,2,timenow2,myStyle_centre)
        mySheet.write(i-5+3,3,i,myStyle_centre)
        mySheet.write(i-5+3,4,similarity_value,myStyle)
        
        if similarity_value<=0.7:
            pass
            #mySheet.write(i-5+3,5,"存在卡顿！",myStyle_centre)
        if (similarity_value>0.7) & (similarity_value < 0.8):
            pass
            #mySheet.write(i-5+3,5,"存在疑似卡顿！",myStyle_centre)
        if i%30==0:
            pass
            #myWorkbook.save('robot moving jammed'+ '.xls')
        i=i+1
        time.sleep(0.02)