# encoding: utf-8

"""
功能：把 markdown 文章格式化为jekyll post。
工作环境：windows
原理：
1. 扫描我的文档目录，查找 markdown 文件。
2. 按照jekyll 要求添加内容header
3. 文件rename, 按照jekyll 要求格式化文件名称

"""

import os
import time

# 文档所在的目录
PATH = 'C:/Users/yangpan3/Documents'


def get_file_mtime(file_path):
    """
    获取文件的创建时间（格式：%Y-%m-%d %H:%M:%S）
    @param file_path: 文件路径
    @return: 2023-03-29 10:17:20
    """
    m_ti = time.ctime(os.path.getmtime(file_path))

    # Using the timestamp string to create a
    # time object/structure
    t_obj = time.strptime(m_ti)

    # Transforming the time object to a timestamp
    # of ISO 8601 format
    return time.strftime("%Y-%m-%d %H:%M:%S", t_obj)


def name_format(file_name, prefix):
    """
    按照jekyll 要求格式化文件名称
    :param file_name: 
    :param prefix: 文件创建时间 2023-03-29 10:17:20
    """
    format_file_name = '{}-{}'.format(prefix[0: 10], file_name.replace(' ', '-'))
    os.rename(os.path.join(PATH, filename), os.path.join(PATH, format_file_name))
    print('final file {}'.format(format_file_name))


def append_yaml(file_name):
    """
    按照jekyll 要求添加内容header
    """
    print('process file {}'.format(file_name))
    file_path = os.path.join(PATH, file_name)
    modify_time = get_file_mtime(file_path)
    with open(file_path, 'r+', encoding='UTF-8') as file:
        content = file.read()
        file.seek(0, 0)
        file.write('---\n')
        file.write('layout: post\n')
        file.write('title:  "{}"\n'.format(file_name[0: file_name.find('.')]))
        file.write('date:   {} +0800\n'.format(modify_time))
        # 目前已有的分类： 学习笔记 源码阅读 实战问题 算法
        file.write('categories: 源码阅读\n')
        # 默认取标题生成 tags
        file.write('tags: {}\n'.format(file_name.replace("-", " ")))
        file.write('---\n')
        file.write('\n')
        file.write('* content\n')
        file.write('{:toc}\n')
        file.write('\n')
        file.write(content)
    name_format(file_name, modify_time)


if __name__ == '__main__':
    for filename in os.listdir(PATH):
        # print filename
        if filename.endswith('md') or filename.endswith('markdown'):
            print('find file {}'.format(filename))
            append_yaml(filename)
