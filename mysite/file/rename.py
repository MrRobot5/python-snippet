# -*- coding:utf-8 -*-
# 批量处理文件 rename
# @since 2016/8/25

import os

PATH = 'e:/export/_posts'


def filename_format():
    for filename in os.listdir(PATH):
        # filename.find('txt') != -1 and len(filename.split(' ')) == 2
        if filename.startswith('20') and filename.endswith('md'):
            title = filename[0: filename.find('.')]
            print(title)
            os.rename(os.path.join(PATH, filename), os.path.join(PATH, filename.replace('笔记', 'Note')))


if __name__ == '__main__':
    filename_format()
