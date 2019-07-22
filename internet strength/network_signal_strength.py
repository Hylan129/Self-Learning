import subprocess
import time
import datetime
import re
import csv

client_msg = "netsh wlan show interfaces"

pattern = re.compile("\s+(\w+\s?\(?\w+?\)?)\s+:\s(\w+\%?\s?\-?\w*:?\w?\w?:?\w?\w?:?\w?\w?:?\w?\w?:?\w?\w?)")
head  = ['Time','SSID','BSSID','状态','信道','信号','接收速率(Mbps)','传输速率 (Mbps)']
while(True):

    res = subprocess.Popen(client_msg,shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res_err = res.stderr.read()
    
    try:
        if res_err:
            cmd_res = res_err
            
            with open('wifi_information_records.txt','a') as result:
                result.write("\n******"+str(timenow)+"******"+cmd_res.decode('gbk',errors ='ignore')+'\n')
        else:
            cmd_res = res.stdout.read()
            content = cmd_res.decode('gbk',errors ='ignore')
       
            dict_content = {}
            for line in content.split('\n'):
                if not line.strip(): continue
                result_content = pattern.findall(line.strip('\r'))
                #print(result_content)
                if result_content != []:
                    name,cont = result_content[0]
                    dict_content[name]=cont
            print(dict_content)
            
            need_content_id = ['SSID','BSSID','状态','信道','信号','接收速率(Mbps)','传输速率 (Mbps)']
            need_content =''
            
            for need in need_content_id:
                need_content = need_content + need + ":" + dict_content[need] + ','
                        
            with open('wifi_information_records.txt','a') as result:
                
                result.write("\n******"+str(timenow)+"******"+'\n'+''.join(need_content)+'\n')
            
            with open('wifi_information_records.csv','a',newline='') as result_csv:
                write_csv = csv.writer(result_csv,dialect='excel')
                if head !=[]:
                    write_csv.writerow(head)
                    head = []
                write_csv.writerow([str(timenow),dict_content['SSID'],dict_content['BSSID'],dict_content['状态'],dict_content['信道'],dict_content['信号'],dict_content['接收速率(Mbps)'],dict_content['传输速率 (Mbps)']])
            
        time.sleep(2)
    except Exception as e:
        with open('wifi_information_records.txt','a') as result:
            result.write("\n程序运行异常："+ str(e)+'\n')