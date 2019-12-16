# -*- coding: utf-8 -*-
from cv2 import cv2
from win32api import GetSystemMetrics
#from cv2 import VideoCapture,imwrite

width,height = GetSystemMetrics(0),GetSystemMetrics(1)
def getPicture():
    try:
        capture = cv2.VideoCapture(0)
        capture.set(3,width)
        capture.set(4,height)
        ret, frame = capture.read()
        cv2.imwrite("files/foreward" +'.jpg',frame)
    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "拍照故障！\n")
        return False
    finally:
        cv2.destroyAllWindows()
    return True