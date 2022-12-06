# -*- coding:utf-8 -*-
""" isnumeric.py
test a numeric string s if it's usable for int(s) or float(s)
"""

def isnumeric(s):
    """returns True if string s is numeric"""
    return all(c in "0123456789.+-" for c in s)

# test module ...
if __name__ == '__main__':
    print(isnumeric('123'))      # True
    print(isnumeric('-123.45'))  # True
    print(isnumeric('+3.14'))    # True
    print(isnumeric('$99.95'))   # False
# 该代码片段来自于: http://www.sharejs.com/codes/python/8269

target = open('d:/log2.txt', 'w')
with open("d:/log.txt") as f:
    for line in f:
        if isnumeric(line.strip()):
            target.writelines(line)
        else:
            target.write(line)
        print line.decode('gbk')

target.close()

