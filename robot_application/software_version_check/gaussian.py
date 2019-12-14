import requests,json

def getGaussianVersion(url):

    version_init = json.loads(requests.get(url).content)
    gaussian_information = ''
    if version_init['msg'] == 'successed':
        for m in version_init['data'].values():
            gaussian_information += "<td>" + str(m) + "</td>"
    else:
        gaussian_information = "<td>高仙底盘通讯异常！</td>"

    return  "<tr><td>0</td>" + gaussian_information + "</tr>"
    