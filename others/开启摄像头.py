# 打开摄像头并灰度化显示
import cv2

capture = cv2.VideoCapture(0)
capture.set(3,1366)
capture.set(4,768)

i = 0

while(True):
    # 获取一帧
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', gray)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite(str(i)+'.jpeg',frame)
        i=i+1
        print(cv2.waitKey(1),str(cv2.waitKey(1)),int(cv2.waitKey(1)))
        
