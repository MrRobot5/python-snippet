# -*- coding: UTF-8 -*-

# python解析照片拍摄时间整理图片


import os
import re
import time
import shutil
import exifread


def rename_pic(root_dir, filename):
    file_path = os.path.join(root_dir, filename)
    try:
        file_rename = filename
        with open(file_path, 'rb') as file_data:
            tags = exifread.process_file(file_data)
            tag_date = 'EXIF DateTimeOriginal'
            if tag_date in tags:
                file_rename = str(tags[tag_date]).replace(':', '').replace(' ', '_') + os.path.splitext(filename)[1]
            else:
                print('No {} found'.format(tag_date), ' in: ', file_path)
        new_path = os.path.join(root_dir, file_rename)
        if not os.path.exists(new_path):
            print(file_path, new_path)
            os.rename(file_path, new_path)
    except Exception as e:
        print("error ", e)


def rename_video(root_dir, filename):
    format = '%Y%m%d_%H%M%S'
    file_path = os.path.join(root_dir, filename)
    statinfo = os.stat(file_path)
    temp_time = time.localtime(statinfo.st_mtime)
    file_rename = str(time.strftime(format, temp_time)) + os.path.splitext(filename)[1]
    new_path = os.path.join(root_dir, file_rename)
    if not os.path.exists(new_path):
        os.rename(file_path, new_path)


def rename(root_dir):
    img_reg = r'(\.JPG|\.PNG|\.jpg|\.png)'
    video_reg = r'(\.mp4|\.MP4|\.MOV)'
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)
        if os.path.isfile(file_path):
            if re.search(img_reg, filename):
                rename_pic(root_dir, filename)
            elif re.search(video_reg, filename):
                rename_video(root_dir, filename)


def save_files(root_dir, save_dir):
    for filename in os.listdir(root_dir):
        try:
            time_info = os.path.splitext(filename)[0].split("_")[0]
            dst_dir = save_dir + time_info
            if not os.path.exists(dst_dir):
                os.mkdir(dst_dir)
            src_path = os.path.join(root_dir, filename)
            save_path = os.path.join(dst_dir, filename)
            print(src_path, save_path)
            shutil.move(src_path, save_path)
        except Exception as e:
            print("error ", e)


if __name__ == '__main__':
    root_dir = r"D:/"
    save_dir = "/Users/xxx/Downloads/"
    rename(root_dir)
    # save_files(root_dir, save_dir)

