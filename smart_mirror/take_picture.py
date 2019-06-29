# -*- coding: utf-8 -*-
from cv2 import VideoCapture,cvtColor,imshow,imwrite,COLOR_BGR2BGRA,waitKey
from os import getcwd,system,mkdir,path
import qrcode_make

capture = VideoCapture(0)

picturenames=["face","leftside","rightside","back"]
picturenames_cn=["正面照","左侧照","右侧照","背影照"]

i = 0
if not path.exists(getcwd()+"\qr"):
    mkdir((getcwd()+"\qr"))
if not path.exists(getcwd()+"\picture"):
    mkdir(getcwd()+"\picture")
print("请点击Enter开始拍照！！！\n\n")
while(True):
    # 获取一帧
    ret, frame = capture.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cvtColor(frame,COLOR_BGR2BGRA)

    #cv2.imshow('frame', gray)
    imshow('Press Enter to take picture !',gray)
    
    if waitKey(1) == ord('\r'):
        if i>(len(picturenames)-1):
            break;
        picturename = picturenames[i]
        imwrite("picture/" + picturename +'.jpeg',frame)
        i = i+1
        print("第%d张照片已拍摄完成，%s！" %(i,picturenames_cn[i-1]))
        if i==len(picturenames):
            print("\n\n照片拍摄完成，请按Enter退出，并查看照片！")
for picture in picturenames:
    qrcode_make.qrcode_produce(getcwd()+ "\\\\qr\\" + picture+ "qr",picture)

system("mirror_picture.html")
