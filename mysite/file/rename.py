# -*- coding:utf-8 -*-
# 批量处理文件 rename
# @since 2016/8/25

import os

path = 'D:/dongdongFile/interview'
for file in os.listdir(path):
    filename = file.decode('gbk')
    #print(filename)
    if (filename.find('txt') != -1 and len(filename.split(' ')) == 2):
        title = filename[0: filename.find('.txt')]
        new = title.split(' ')[1] + ' ' + title.split(' ')[0] + '.txt'
        print(new)
        os.rename(os.path.join(path, filename), os.path.join(path, new))