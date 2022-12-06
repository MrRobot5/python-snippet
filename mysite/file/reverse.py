# -*- coding: UTF-8 -*-

#Read file
path = raw_input("需要转换的文件路径：")

original = open(path, "r")
print "o 文件名：", original.name
newpath = path[0: path.rindex('/')] + "/reverse.txt"
print "r 文件名：", newpath

target = open(newpath, 'w')
AllLines = original.readlines()
AllLines.reverse()

for EachLine in AllLines:
    target.write(EachLine.lstrip())

target.close()
original.close()

print "reverse file close!"
