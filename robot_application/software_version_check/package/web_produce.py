from package import file_version,take_picture

def makePage(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting,sixmic_info,FourG_Info):

    web_page = open("files/html_base.html",encoding='utf-8').read().replace("\n",'')
    
    resolution_setting = str(take_picture.width) + "*" + str(take_picture.height)

    if not take_picture.getPicture():
        final_web_page = web_page.format(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting,
            resolution_setting,'','','拍照失败！',sixmic_info,FourG_Info)
    else:
        picture_status = file_version.getFileSizeandTime("files/foreward.jpg")
        final_web_page = web_page.format(logo,Mname,Mcode,ip_list,timenow,robot_setting,gaussian_setting,
            resolution_setting,
            picture_status[0],
            picture_status[1],'拍照成功！',sixmic_info,FourG_Info)

    return final_web_page
