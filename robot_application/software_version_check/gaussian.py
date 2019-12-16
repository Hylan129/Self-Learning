import requests,json

def getGaussianVersion(url):

    version_init = json.loads(requests.get(url).content)
    gaussian_information = ''
    if version_init['msg'] == 'successed':

        need_data = version_init['data']
        temp = ''
        try:
            temp = need_data['laser_serial_number']
            del need_data['hardwareVersion5'],need_data['diskAvailable'],need_data['diskCapacity'],need_data['laser_serial_number'],need_data["systemVersion"]
        except:
            pass
        for m in need_data.values():
            gaussian_information += "<td>" + str(m) + "</td>"
    else:
        gaussian_information = "<td>高仙底盘通讯异常！</td>"

    return  "<tr>" + gaussian_information + "<td>" + temp + "</td></tr>"
    