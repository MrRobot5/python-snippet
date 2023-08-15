# -*- coding:utf-8 -*-
# 批量处理文件 rename
# @since 2016/8/25

"""
使用 shell rename 命令进行替换：
rename 's/笔记/note/' $PATH/*
将 PATH 替换为你要进行替换的文件夹路径。执行脚本后，它将替换文件夹中所有文件名中的"笔记"为"note"。
@since 2023-08-04 15:22:17 chat-gpt
"""

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
