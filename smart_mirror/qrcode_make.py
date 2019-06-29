#!/usr/bin/python
# -*- coding: UTF-8 -*-

from qrcode import QRCode,constants

def qrcode_produce(url,name):
    qr = QRCode(     
        version=1,     
        error_correction=constants.ERROR_CORRECT_L,     
        box_size=5,     
        border=4, 
    ) 
    qr.add_data(url) 
    qr.make(fit=True)  
    img = qr.make_image()
    img.save("qr/"+ name + "qr.png")
