# -*- coding: UTF-8 -*-

import os
import shutil

"""
使用 python 脚本，实现不同目录下的文件对比和拷贝。

@since: 2023年11月6日16:14:16
@author: chat-gpt 
"""


def get_files_from_dir(base_dir):
    """
    yield是Python中的一个关键字，它在函数中的作用类似于return，
    但有一个重要的区别：yield会产生一个值，但不会结束函数的执行，而是将函数暂停并保存当前的所有状态（包括变量值等），以便在下次从这个点继续执行。
    这样的函数被称为生成器（generator）。
    @param base_dir:
    @return:
    """
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            yield file  # 只返回文件名，不返回完整路径


def copy_files_not_in_dir(src_dir, dest_dir):
    """
    这个脚本将递归遍历 src_dir 和 dest_dir 目录，如果在 src_dir 目录中找到 dest_dir 目录中不存在的文件，它将复制这些文件到 dest_dir 目录。
    这个脚本假设你的目录结构是扁平的，也就是说，它不会保留原始的子目录结构。
    注意：这个脚本使用了os.walk函数来递归遍历目录，shutil.copy函数来复制文件。在运行这个脚本之前，请确保你有足够的权限来读取源目录和写入目标目录。

    @return:
    """
    src_files = set(get_files_from_dir(src_dir))
    dest_files = set(get_files_from_dir(dest_dir))

    files_to_copy = src_files - dest_files

    for file in files_to_copy:
        src_file_path = os.path.join(src_dir, file)
        dest_file_path = os.path.join(dest_dir, file)
        if os.path.isfile(src_file_path):
            shutil.copy(src_file_path, dest_file_path)


if __name__ == '__main__':
    copy_files_not_in_dir(r"D:\export\7", r"D:\export\6")
