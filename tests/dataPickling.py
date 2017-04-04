try:
    import cPickle as pickle
except ImportError:
    import pickle
import os
import json

localPath = os.path.split(os.path.realpath(__file__))[0]

d = dict(name = 'asahi', age = '17', score = 95)
d2 = {'name' : 'luna', 'age' : 16, 'score' : 100}

with open(''.join(localPath) + '\\dataSave.txt', 'wb') as f:
    pickle.dump(d, f)
    pickle.dump(d2, f)
    
with open(''.join(localPath) + '\\dataSave.txt', 'rb') as f2:
    d3 = pickle.load(f2)
    d4 = pickle.load(f2)

print d3, d4

dj = dict(name = 'sakura', age = '89', score = '97')
print json.dumps(dj)

class MsgUnit(object):
    def __init__(self, time, userID, msgType, msgContent):
        self.time = time
        self.userID = userID
        self.msgType = msgType
        self.msgContent = msgContent
        
def json2MsgUnit(d):
        return MsgUnit(d['time'], d['userID'], d['msgType'], d['msgContent'])

testMsg = MsgUnit('<2017.04.05 00:18:50>', 'asuna', 'public', 'hello,everyone')
with open(''.join(localPath) + '\\classSave.json', 'wb') as f3:
        json.dump(testMsg, f3, default = lambda obj: obj.__dict__)
        
with open(''.join(localPath) + '\\classSave.json', 'rb') as f4:
        str = f4.readline()
testMsg = json.loads(str, object_hook = json2MsgUnit)
print testMsg.time + testMsg.userID + ':' + testMsg.msgContent
