# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 08:13:43 2017
@author: dc
"""
 
import http.server as hs
import sys, os
import socket
import urllib.request
import requests
import socketserver
 
 
class ServerException(Exception):
 
    '''服务器内部错误'''
 
    pass
    
class RequestHandler(hs.BaseHTTPRequestHandler):
    
    def send_content(self, page, status = 2000):
    
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        #self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(bytes(page, encoding = 'utf-8'))
    
    def do_GET(self):
        #这里要处理两个异常，一个是读入路径时可能出现的异常，一个是读入路径后若不是文件，要作为异常处理    
        #lists = os.listdir() + str(self.path.replace("/","\\"))
        fullpath = os.getcwd() + urllib.request.url2pathname(str(self.path.replace("/","\\")))
        print(fullpath)
        if not os.path.exists(fullpath):
            print("路径：%s不存在！"%fullpath)
        elif os.path.isfile(fullpath):
            
            #urllib.request.urlretrieve(urllib.request.pathname2url(fullpath),fullpath.split('\\')[-1])
            #urllib.request.urlretrieve("http://www.baidu.com",fullpath.split('\\')[-1])
            #print(urllib.request.pathname2url(fullpath))
            #self.handle_file(fullpath)
            #url = "file:" + urllib.request.pathname2url(fullpath)
            url = urllib.request.pathname2url(fullpath).strip("/")
            print(url)
            print(self.path)
            #content0 = "<li><a href=" + "file://localhost/" + fullpath.replace("\\","\\\\") + ">" + self.path + "</a></li>"
            content0 = "<li><a href=" + "\".."+self.path + "\">" + self.path + "</a></li>"
            print(content0)
            msg = content0
            self.handle_error(msg)
            
            #self.handle_file(fullpath)
            
        else:
            lists = os.listdir(fullpath)
            print(lists)
            print(self.path)
            content0 = ""
            number = 1
            for list in lists:
                if self.path=="/":
                    content0 = content0 +"<li><a href=" + list.replace(" ","%20") + ">" + str(number) + "-->" + list + "</a></li>"
                else:
                    content0 = content0 +"<li><a href=" + urllib.request.url2pathname(str(self.path.replace("/","\\")))+ "\\"+list.replace(" ","%20") + ">" + str(number) + "-->" + list + "</a></li>"

                number = number + 1
            msg = content0
            self.handle_error(msg)
        
    def handle_file(self, full_path):
        
        try:
            #file= urllib.request.urlopen("file:" + urllib.request.pathname2url(full_path))
            #file = requests.get("file:" + urllib.request.pathname2url(full_path))
            file = requests.get("http://192.168.0.105:8030/calc.exe")
            print(urllib.request.pathname2url(full_path))
            #content = file.read()
            with open("hylan.txt", 'wb') as code:
            
                code.write(file.content)
                
                print("已经写入！")
            
                #self.send_content(content,200)
        
        except IOError as msg:
            
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            
            self.handle_error(msg)
         
    
    Error_Page = """<html><head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Directory listing for  /</title>
            </head>
            <body>
            <h1>Directory listing for /</h1>
            <hr>
                <ul>
                {msg}
                </ul>
            <hr>
            </body></html>"""
        
    def handle_error(self, msg):
    
        content = self.Error_Page.format(msg= msg)
        self.send_content(content, 404)
        
if __name__ == '__main__': 
    
    ip = socket.gethostbyname(socket.gethostname())
    httpAddress = (ip, 8030)
    print("ip: %s" % ip)
    httpd = hs.HTTPServer(httpAddress, RequestHandler)
    httpd.serve_forever()
