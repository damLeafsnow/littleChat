try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import time
localPath = os.path.split(os.path.realpath(__file__))[0]

msg = {
    'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    'username' : 'luna',
    'msgType' : 'public',
    'msgContent' : u'测试一下中文'
    }
    
msg2 = {
    'time' : time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    'username' : 'asahi',
    'msgType' : 'private',
    'msgContent' : u'日本のテスト'
    }

def printMsg(message):
    if message['msgType'] == 'public':
        print '<' + message['time'] + '>' + message['username'] + ':' + message['msgContent']
    elif message['msgType'] == 'private':
        print '[Pvt]' + '<' + message['time'] + '>' + message['username'] + ':' + message['msgContent']
    
#printMsg(msg)

with open(''.join(localPath) + '\\msgdata', 'w') as f:
    pickle.dump(msg, f)
    pickle.dump(msg2, f)
    
with open(''.join(localPath) + '\\msgdata', 'r') as f2:
    while True:
        try:
            d = pickle.load(f2)
            printMsg(d)
        except EOFError:
            break
