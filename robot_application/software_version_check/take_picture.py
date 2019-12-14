# -*- coding: utf-8 -*-
from cv2 import cv2
#from cv2 import VideoCapture,imwrite

def getPicture():
    try:
        capture = cv2.VideoCapture(0)
        capture.set(3,1366)
        capture.set(4,768)
        ret, frame = capture.read()
        cv2.imwrite("files/foreward" +'.jpg',frame)
    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "拍照故障！\n")
        return False
    finally:
        cv2.destroyAllWindows()
    return True