# -*- coding: utf-8 -*-

try:
    from urllib import request
    from time import sleep
    from urllib.parse import urlencode
    from pandas import read_excel
except Exception as e:
    print(str(e))
    input('1exit')

def sixmic(equip_no,set_no,strValue,ip):

    server_login = 'http://' + ip + ':8088/GWService.asmx/LoginService?userName=admin&userPwd=admin'
    sixmic_use2 = "http://" + ip + ":8088/GWService.asmx/SetupsCommand2?"
        
    req_admin = request.Request(server_login)
    res_admin = request.urlopen(req_admin)
    res_admin.close()
    
    talk_parm = {"equip_no":equip_no,"setNo":set_no,"strValue":strValue}
    req_talk = request.Request(sixmic_use2 + urlencode(talk_parm))
    res_talk = request.urlopen(req_talk)
    res_talk.close()
    

if __name__ == '__main__':
    try:
    
        content = read_excel('robot_talk.xls')
        ip1,ip2 = content['robot_1'][0],content['robot_2'][0]
        
        input('点击 ENter 开始讲解！')
        
        if len(ip1.split('.')) == len(ip2.split('.')) == 4:
            
            try:
            
                while True:
                    for i,j in zip(content['robot_1'][1:],content['robot_2'][1:]) :
                        
                        sixmic('6','3',i,ip1)
                        
                        sleep(0.3 * len(i))
                        
                        sixmic('6','3',j,ip2)
                        
                        sleep(0.3 * len(j))
                        
                    input('点击 ENter 继续讲解！')
                    
            except Exception as e:
                with open('program_error.txt','a') as result:
                    result.write("\n************"+ str(e) +'main\n')
        else :
            print('robot_talk配置为空！')
            input('Enter To Exit！')
    except Exception as e:
        print(str(e))
        input('2exit')