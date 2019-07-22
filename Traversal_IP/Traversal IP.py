import subprocess
import socket
import os

ip = socket.gethostbyname(socket.gethostname())

client_msg_head = '.'.join([x for x in ip.split('.')[:-1]])

for num in range(1,255):
    client_msg = "adb connect " +client_msg_head +'.' + str(num)
    ping_msg = "ping -n 1 -w 1 " +  client_msg_head +'.' + str(num)
    
    if os.system(ping_msg)==0:
        res = subprocess.Popen(client_msg,shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        res_err = res.stderr.read()
        if res_err:
            cmd_res = res_err
        else:
            cmd_res = res.stdout.read()
        with open('result.txt','a') as result:
            result.write(client_msg+cmd_res.decode())
        print(client_msg)
