import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 9527))

print s.recv(1024)
for data in ['kokura asahi', 'sakurakouji runa', 'ursule fleur jeanmaire', 'ookura resona']:
    s.send(data)
    print s.recv(1024)
s.send('exit')
s.close()