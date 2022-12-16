# encoding: utf-8

import os
import time

# 文档所在的目录
PATH = '/Users'


def get_file_mtime(file_path):

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
    :param prefix: 
    """
    os.rename(os.path.join(PATH, filename), os.path.join(PATH, '{}-{}'.format(prefix[0: 10], file_name.replace(' ', '-'))))


def append_yaml(file_name):
    """
    按照jekyll 要求添加内容header
    """
    print('append file {}'.format(file_name))
    file_path = os.path.join(PATH, file_name)
    modify_time = get_file_mtime(file_path)
    with open(file_path, 'r+', encoding='UTF-8') as file:
        content = file.read()
        file.seek(0, 0)
        file.write('---\n')
        file.write('layout: post\n')
        file.write('title:  "{}"\n'.format(file_name[0: file_name.find('.')]))
        file.write('date:   {} +0800\n'.format(modify_time))
        file.write('categories: jekyll update\n')
        file.write('---\n')
        file.write('\n')
        file.write(content)
    name_format(file_name, modify_time)


if __name__ == '__main__':
    for filename in os.listdir(PATH):
        # print filename
        if filename.endswith('md') or filename.endswith('markdown'):
            append_yaml(filename)
