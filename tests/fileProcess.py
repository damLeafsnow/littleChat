import os
localFile = pathname = os.path.split(os.path.realpath(__file__))[0]
with open(''.join(localFile) + '\\test.txt', 'a') as f:
    for i in (0, 1, 2, 3, 4, 5):
        f.write('test%d, and hello,world!\n' % i)
with open(''.join(localFile) + '\\test.txt', 'r') as f2:
    list = f2.readlines()
for str in list:
    print str