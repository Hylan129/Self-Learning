import serial,time
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
        self.ser.open()            #打开串口,要找到对的串口号才会成功
        if not self.ser.isOpen():
            with open('error.txt','a') as code:
                code.write("4G板串口连接出错！\n")
            
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
        try:
            command = 'AT+CWSSID?\r\r\n'
            self.ser.read_all()
            self.send(bi.hexlify(command.encode()).decode())
            time.sleep(2)
            feedbacks = self.ser.read_all().decode().split("\n")
            feedbacks_deal = [fb.strip() for fb in feedbacks if fb.strip() != '']
            self.port_close() 
            if feedbacks_deal[2].upper() == 'OK':
                return [self.ser.port,feedbacks_deal[1][8:]]
            else:
                return [self.ser.port,FourG_WiFi]
        except Exception as e:
            with open('error.txt','a') as code:
                code.write("4G板串口连接出错！" + str(e) + "\n")
            return [self.ser.port,FourG_WiFi]