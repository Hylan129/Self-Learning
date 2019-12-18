import serial,os,time
import binascii as bi

FourG_WiFi = "查询失败！"

class FourGMod(object):

    def __init__(self,com_port):
        self.ser = serial.Serial() 
        self.ser.port = com_port      #设置端口号
        self.ser.baudrate = 115200   #设置波特率
        self.ser.bytesize = 8        #设置数据位
        self.ser.stopbits = 1        #设置停止位
        self.ser.parity = "N"        #设置校验位
        try:
            self.ser.open()            #打开串口,要找到对的串口号才会成功
            if not self.ser.isOpen():
                with open('error.txt','a') as code:
                    code.write("4G板串口连接出错！\n")
        except Exception as e:
            with open('error.txt','a') as code:
                    code.write(str(e) + "4G板串口连接！\n")
            
    def port_close(self):
        self.ser.close()
        if self.ser.isOpen():
            return True
        else:
            return False
            
    def send(self,send_data):
        if (self.ser.isOpen()):
            self.ser.write(bytes.fromhex(send_data)) #Hex发送
        else:
            self.ser.open()
            self.ser.write(bytes.fromhex(send_data)) #Hex发送
    def setting_4G_WIFI(self,wifi_name):
        command = 'AT+CWSSID = "'+ wifi_name + '"\r\r\n'
        self.send(bi.hexlify(command.encode()).decode())
        return True

    def control_4G_WIFI(self,sign):
        command = 'AT+CWMAP = "'+ sign + '"\r\r\n'
        self.send(bi.hexlify(command.encode()).decode())
        return True

    def check_4G_WIFI(self):
        command = 'AT+CWSSID?\r\r\n'
        self.ser.read_all()
        self.send(bi.hexlify(command.encode()).decode())
        time.sleep(2)
        feedbacks = self.ser.read_all().decode().split("\n")
        feedbacks_deal = [fb.strip() for fb in feedbacks if fb.strip() != '']
        if feedbacks_deal[2].upper() == 'OK':
            return feedbacks_deal[1][8:]
        else:
            return FourG_WiFi
if __name__ == "__main__":
    try:
        os.system("taskkill /f /im AlarmCenterMonitorService.exe")
        time.sleep(1)

        print("\n【4G板WIFI名称更改设置...名称不能包含中文字符，不能为空】")
        wifi_model = FourGMod(open('config.txt').read().strip())
        try:
            print("\n当前WIFI名称：" + wifi_model.check_4G_WIFI())
        except:
            wifi_model.setting_4G_WIFI("WaitToUpdateName")
            time.sleep(7)
            print("\nWIFI名称包含中文字符，已重置为：WaitToUpdateName")

        wifi_model.control_4G_WIFI('1')
        input("\nEnter to Continue")

        para = input("\n输入新的WIFI名称：").strip()
        while(True):
            if para != '':
                wifi_model.setting_4G_WIFI(para)
                time.sleep(7)
                input("\n名称已更改！点击Enter查阅更改后的名称.")

                try:
                    print("\n当前WIFI名称：" + wifi_model.check_4G_WIFI())
                    input("\nEnter TO EXIT!")
                    break
                except:
                    wifi_model.setting_4G_WIFI("WaitToUpdateName")
                    time.sleep(7)
                    para = input("\n输入名称异常，已重置为：WaitToUpdateName,请重新输入：")
            else:
                para = input("\n输入名称为空，请重新输入：")
            
        wifi_model.control_4G_WIFI('0')
        time.sleep(1)
        while(wifi_model.port_close()):
            time.sleep(0.5)

    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "\n main")