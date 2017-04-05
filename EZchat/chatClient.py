import socket
import threading
import string
import sys
try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time
localPath = os.path.split(os.path.realpath(__file__))[0]

#输入处理,<yooo>怎么去掉、、
def prompt():
    sys.stdout.write('<you>')
    sys.stdout.flush()

#处理信息并输出
def printMsg(message):
    sys.stdout.flush()
    if message['msgType'] == 'public':
        print '<' + message['time'] + '>' + message['username'] + ':' + message['msgContent']
    elif message['msgType'] == 'private':
        print '[Pvt]' + '<' + message['time'] + '>' + message['username'] + ':' + message['msgContent']

#监听数据
def listeningMsg(s):
    while True:
    #incoming messages
        data = s.recv(4096)
        if not data:
            print '\nDisconnected from chat server'
            exit()
        else:
            msg = pickle.loads(data)
            printMsg(msg)
            prompt()


if __name__ == "__main__":
    #if(len(sys.argv) < 3):
    #    print 'Usage : python chatClient.py hostname port'
    #    sys.exit()
        
    host = "127.0.0.1"#sys.argv[1]
    port = 8848#int(sys.argv[2])
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(2)#阻塞超时时间
    
    #connect
    try:
        s.connect((host, port))
    except:
        print 'Unabel to connect'
        sys.exit()
        
    print 'Connected to remote host.Start sending messages'
    prompt()#目测是在前面加<you>提示符并且清理缓冲
    
    t = threading.Thread(target = listeningMsg, args = (s,))
    t.start()
    
    while True:
        #user input
        str = raw_input()
        s.send(str)
        prompt()
    s.close()

