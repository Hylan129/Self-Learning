#!/usr/bin/python
# -*- coding: UTF-8 -*-

from qrcode import QRCode,constants
import os

def qrcode_produce(url):
    qr = QRCode(     
        version=1,     
        error_correction=constants.ERROR_CORRECT_L,     
        box_size=10,     
        border=4, 
    ) 
    qr.add_data(url) 
    qr.make(fit=True)  
    img = qr.make_image()
    img.save("qrcode.png")

qr_content = input("\n请输入需要转二维码的内容，拖动TXT文件路径也可以。\n\nPS：TXT文件中文字数超过1000字无效！\n\n开始输入：").strip("\"")

try:
    if os.path.isfile(qr_content)&(qr_content.split(".")[1]=="txt"):
        content = open(qr_content).read()
        qrcode_produce(content)
        os.system("qrcode.png")
        input("\nTXT文本转二维码成功，TXT文本字节数：%d ，请按ENTER结束！"% len(content))
except:
#else:
    qrcode_produce(qr_content)
    os.system("qrcode.png")
    input("\nTXT文本超过1000字或者输入路径非TXT文本路径，输入内容已转二维码！\n\n输入文本字节数：%d ，请按ENTER结束！"%len(qr_content))


