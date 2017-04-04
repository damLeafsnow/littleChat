import socket
import os

#AF_INET:IPv4 (AF_INET6 : IPv6) SOCK_STREAM : 面向流
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('www.baidu.com', 80))
s.send('GET / HTTP/1.1\r\nHost:www.baidu.com\r\nConnection: close\r\n\r\n')

buffer = []
while True:
    d = s.recv(1024)#1024 Byte one turn
    if d:
        buffer.append(d)
    else:
        break
data = ''.join(buffer)

s.close()

header, html = data.split('\r\n\r\n', 1)
print header

pathname = os.path.split(os.path.realpath(__file__))[0]
with open(''.join(pathname) + '\\baidu.html', 'wb') as f:
    f.write(html)