import file_version,take_picture

def makePage(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting):

    web_page = open("files/html_base.html",encoding='utf-8').read().replace("\n",'')

    if not take_picture.getPicture():
        final_web_page = web_page.format(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting,'','','','拍照失败！')
    else:
        picture_status = file_version.getFileSizeandTime("files/foreward.jpg")
        final_web_page = web_page.format(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting,'1366*768',picture_status[0],picture_status[1],'拍照成功！')

    return final_web_page
