#!/usr/bin/python
# -*- coding: UTF-8 -*-

from qrcode import QRCode,constants

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
    img.save("请扫描二维码获取共享文件.png")
