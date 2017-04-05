import threading
import socket
try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time
localPath = os.path.split(os.path.realpath(__file__))[0]

userDict = {
        "127.0.0.1:4248" : "leafsnow"
        }

#处理客户端信息获得username
def getUserName(addr):
    ip = addr[0]
    port = addr[1]
    key = ip + ":" + str(port)
    for t in userDict.keys():
        if(t == key):
            return userDict[key]
    return key
    
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

        t.start()
        
        print "Client (%s) connected" % getUserName(addr)
        msg = {
            'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            'username' : 'system',
            'msgType' : 'public',
            'msgContent' : "[%s] entered room\n" % getUserName(addr)
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
            try:
                CONNECTION_LIST.remove(sock)
                msg = {
                    'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    'username' : 'system',
                    'msgType' : 'public',
                    'msgContent' : "Client (%s) is offline" % getUserName(addr)
                    }
                broadcast_data(sock, pickle.dumps(msg))
                print "Client (%s) is offline" % getUserName(addr)
                sock.close()
            except ValueError:#处理掉额外删除问题
                pass
                

if __name__ == "__main__":
    #socket descriptors列表
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 8848
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)#max client = 5
    
    CONNECTION_LIST.append(server_socket)
    
    print "Chat server started on port" + str(SERVER_PORT)
    
    startListening()
    
    server_socket.close()
