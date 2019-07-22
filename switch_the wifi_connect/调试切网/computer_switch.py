#!/usr/bin/python
# coding=UTF-8

import time
import binascii
import subprocess,os
import xml.etree.ElementTree as ET

def produce_wlan_ini(f):

    def wrap(ssid,pwd):

        xml_content = ET.parse("QXZN-Qipai-129.xml")

        root = xml_content.getroot()

        default = '{http://www.microsoft.com/networking/WLAN/profile/v1}'

        for elem in root.iter(default+'name'):
            elem.text = ssid
        for elem in root.iter(default+'hex'):
            elem.text = binascii.hexlify(ssid.encode()).decode().upper()
        for elem in root.iter(default+'keyMaterial'):
            elem.text = pwd
        xml_content.write( ssid + '.xml')
        
        return f(ssid,pwd)
    
    return wrap

@produce_wlan_ini
def wifi_switch(ssid,pwd):
    try:
        
        #导入配置文件
        add_ini = 'netsh wlan add profile filename =' + ssid + '.xml'
        
        #切换网络
        switch = 'netsh wlan connect name=' + str(ssid)
        
        res = subprocess.Popen(add_ini,shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        res_err = res.stderr.read()
        if res_err:
            cmd_res1 = res_err
        else:
            cmd_res1 = res.stdout.read()
        #print(cmd_res.decode("gb2312",'replace'))
        
        time.sleep(5)
        
        res2 = subprocess.Popen(switch,shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        res_err2 = res2.stderr.read()
        
        if res_err2:
            cmd_res2 = res_err2
        else:
            cmd_res2 = res2.stdout.read()
        #print(cmd_res.decode("gb2312",'replace'))
        
    except Exception as e:
        with open('err.txt','a') as code:
            code.write("computer_switch:"+str(e)+'\n')
        
    return cmd_res1.decode("gb2312",'replace') + ',' + cmd_res2.decode("gb2312",'replace')