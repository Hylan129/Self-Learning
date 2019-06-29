import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("www.oschina.net", 80))
s.send("GET / HTTP/1.1\r\nHost:www.oschina.net\r\n\r\n".encode("utf-8"))

d = s.recv(1024)
print(d.decode("utf-8","ignore"))
input("exit....")