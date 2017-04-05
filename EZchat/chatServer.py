﻿import threading
import socket
try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time
localPath = os.path.split(os.path.realpath(__file__))[0]

#广播接受到的客户端信息
def broadcast_data(sock, message):
    #排除master socket和数据源socket
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try:
                socket.send(message)
            except:
                #客户端连接异常
                socket.close()
                CONNECTION_LIST.remove(socket)
                
def startListening():
    while True:
        sock, addr = server_socket.accept()
        #create new thread to process
        t = threading.Thread(target = msgIncoming, args = (sock, addr))
        CONNECTION_LIST.append(sock)
        #print "<debug>CONNECTION_LIST: " 
        #print len(CONNECTION_LIST)
        #print CONNECTION_LIST
        t.start()
        
        print "Client (%s, %s) connected" % addr
        msg = {
            'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'username' : 'system',
            'msgType' : 'public',
            'msgContent' : "[%s:%s] entered room\n" % addr
            }
        broadcast_data(sock, pickle.dumps(msg))

def msgIncoming(sock, addr):
    while True:
        try:
            data = sock.recv(RECV_BUFFER)
            if data:
                msg = {
                    'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'username' : str(sock.getpeername()),
                    'msgType' : 'public',
                    'msgContent' : data
                    }
                broadcast_data(sock, pickle.dumps(msg))
        except:
            msg = {
                'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                'username' : 'system',
                'msgType' : 'public',
                'msgContent' : "Client (%s, %s) is offline" % addr
                }
            broadcast_data(sock, pickle.dumps(msg))
            print "Client (%s, %s) is offline" % addr
            sock.close()
            CONNECTION_LIST.remove(sock)

if __name__ == "__main__":
    #socket descriptors列表
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 8848
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", PORT))
    server_socket.listen(5)#max client = 5
    
    CONNECTION_LIST.append(server_socket)
    
    print "Chat server started on port" + str(PORT)
    
    startListening()
    
    server_socket.close()
