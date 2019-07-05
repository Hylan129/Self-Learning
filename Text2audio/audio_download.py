#audio auto download
#！/usr/bin/env python3
#-*-coding: UTF-8 -*-

import requests
import configparser

config = configparser.ConfigParser()

config.readfp(open(r'setting.ini'))
person = config.get("param_setting","person")
volum = config.get("param_setting","volum")
speed = config.get("param_setting","speed")
pit = config.get("param_setting","pit")

#待转换文本名称
mp3_name = config.get("param_setting","file_name").split('|')

#待转换文本
content_to_tranfer_all = config.get("param_setting","content").split('|')

url_head = 'http://tsn.baidu.com/text2audio?lan=zh&cuid=50-5B-C2-C8-DA-27&tok=24.4a9bc5880ca5fadf2501f058a9730cf9.2592000.1564830555.282335-16039151&ctp=1&&ie=UTF-8&tex='

if len(mp3_name)!=len(content_to_tranfer_all):
    print("文本数量与需保存的文件数量不符，请重新检查后再试！")
else:
    print("文本已经开始转换.....\n\n")
    for i in range(len(mp3_name)):
        content_to_tranfer=content_to_tranfer_all[i]
        Download_addres=url_head+content_to_tranfer+'&per='+person+'&vol='+volum+'&spd='+speed+'&pit='+pit
        #把下载地址发送给requests模块
        f=requests.get(Download_addres)
        #下载文件
        with open('audio/'+mp3_name[i]+'.mp3',"wb") as code:
             code.write(f.content)
        print("Finish："+str(i+1)+"，MP3名称："+mp3_name[i])
print("所有"+str(len(mp3_name))+"个文本内容，已经全部完成音频转换！\n\n")
input('Press Enter to Exit ！')