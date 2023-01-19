# -*- coding: UTF-8 -*-

import glob
import os
import time
import shutil

# 照片copy 的目标文件夹
PHOTOS = r"D:\photos"


def remove_repetition(filenames, filenames_back):
    # 删除重复的文件
    i = 0
    for _ in filenames_back:
        if _.find('(1)') > 0 or _.find('(2)') > 0:
            print(_)
            os.remove(_)
            filenames.remove(_)
            i += 1
    print(i)


def TimeStampToTime(timestamp):
    # 转换时间格式
    timeStruct = time.localtime(timestamp)
    # return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)
    return time.strftime('%Y', timeStruct)


def get_FileCreateTime(filePath):
    # 获取文件创建时间
    # filePath = unicode(filePath,'utf8')
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def My_main():
    # 获取当前文件夹下面的所有文件，不包含文件夹
    filenames = [x for x in glob.iglob("*.*", recursive=False)]
    filenames.remove('solve.py')
    # 设置工作路径
    curr_path = os.getcwd()
    # 去除重复的文件
    filenames_back = filenames[::]
    remove_repetition(filenames, filenames_back)
    # 根据文件的创建时间对文件分类
    for file in filenames:
        os.chdir(curr_path)
        year = get_FileCreateTime(file)
        if not os.path.exists(year):
            os.makedirs(year)
            print('Create ' + year + ' success')
        des_path = year + '/' + file
        shutil.move(file, des_path)  # 移动文件或文件夹


def copy_files_in_one():
    """
    复制 root 以及子目录所有的照片文件到指定目录下
    @rtype: object
    """
    for filepath, dirnames, filenames in os.walk(r'E:\我们的照片'):
        for filename in filenames:
            print(os.path.join(filepath, filename))
            # 新文件path
            new_file = os.path.join(PHOTOS, filename)
            if not os.path.exists(new_file):
                shutil.copyfile(os.path.join(filepath, filename), new_file)


def file_name_check(file_name):
    """
    文件重名检测
    @param file_name: DSC01151.JPG
    @return: 如果文件名重复，则根据文件名累加 DSC01151(1).JPG
    """
    temp_file_name = file_name
    i = 1
    while i:
        if os.path.exists(os.path.join(PHOTOS, temp_file_name)):
            name, suffix = file_name.split('.')
            name += '(' + str(i) + ')'
            temp_file_name = name+'.'+suffix
            i = i+1
        else:
            return temp_file_name


if __name__ == "__main__":
    copy_files_in_one()
    # print(file_name_check("DSC0115333.JPG"))


