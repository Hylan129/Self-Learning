import os,time
import win32api

#输入文件的路径，提前版本信息及大小信息。
def getVersion(fname):
    """
    读取给定文件的所有属性, 返回一个字典.
    """
    propNames = ('ProductName', 'ProductVersion','FileDescription','FileVersion','Comments')
 
    try:
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]
        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            try:
                strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath).strip()
            except :
                strInfo[propName] = 'no information.'
        strInfo['File_Size'] = str(round(os.stat(fname).st_size/1024,2)) + 'KB'
        strInfo['Last_Modify_Time'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(fname).st_mtime))
    except Exception as e:
        with open('error.txt','a') as code:
            code.write(str(e) + "\n")
 
    return strInfo

def getFileSizeandTime(path):
    return (str(round(os.stat(path).st_size/1024,2)) + 'KB',time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.stat(path).st_mtime)))