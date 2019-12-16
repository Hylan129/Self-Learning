import subprocess

def ADBComand(cmd):
    try:
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        res_err = res.stderr.read()
        if res_err:
            cmd_res = res_err.decode('gbk')
        else:
            cmd_res = res.stdout.read().decode('gbk')

        if 'connected' in cmd_res:return True
        return cmd_res
    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "")
        return False

# 信息获取：
#软件名称：adb shell dumpsys package com.iflytek.aiui.devboard.controlservice | findstr versionName
softwares = ["com.iflytek.aiui.devboard.controlservice","com.iflytek.aiuiservice","com.android.launcher"]
#获取所有的软件的版本信息：adb shell dumpsys package * | findstr "\<pkg\> \<versionName\>  \<timeStamp\>"

#mac_address adb shell cat /sys/class/net/wlan0/address
#mic_name adb shell getprop net.hostname
#os_version !adb shell getprop ro.build.version.release

def getSixMic_Information(ip):

    #返回mic_name,mac,os_version,software_version
    #返回所有软件信息，并生成txt，保存在files目录下。sixmic_softwares
    try:
        if ADBComand("adb connect " + ip):
            mic_name = ADBComand("adb shell getprop net.hostname")
            mac_address = ADBComand("adb shell cat /sys/class/net/wlan0/address")
            os_version = ADBComand("adb shell getprop ro.build.version.release")
            softwares_version = [ADBComand("adb shell dumpsys package " + software + " | findstr versionName") for software in softwares]
            # 保存所有的软件信息到文件中。
            ADBComand(r'adb shell dumpsys package * | findstr "\<pkg\> \<versionName\>  \<timeStamp\>" > files/softwares_version.txt')
            return [info.strip() for info in [mic_name,mac_address,os_version] + softwares_version]

        else:
            return ['六麦连接失败！','','','','','']
    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "")
        return ['六麦连接失败！','','','','','']
