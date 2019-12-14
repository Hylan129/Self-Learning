# -*- coding: utf-8 -*-
from cv2 import VideoCapture,imwrite
import cv2

cv2.resizeWindow("Tracking", 800,800)
capture = VideoCapture(0)

capture.set(3, 1366)
capture.set(4, 768)
ret, frame = capture.read()
imwrite("foreward" +'.jpeg',frame)