# -*- coding:utf-8 -*-
import sys
import os
import glob
import random
import pyperclip
import datetime

"""
可以借助 shell alias, 配置脚本。C:/Program Files/Git/etc/bash.bashrc
"""


def find_direct_action():
    """
    查找最新的 hello_time action脚本文件名
    @return: "python temp-20231127-161010.py;"
    """
    # 指定的目录
    directory = '/export/'

    # 获取所有以'tmp'开头的文件
    tmp_files = glob.glob(os.path.join(directory, 'temp*'))

    # 获取最后一个文件，如果存在的话
    if not tmp_files:
        raise Exception("say hello, time👉")

    first_tmp_file = tmp_files[-1]

    # 使用os.path.basename就能从路径中提取包含扩展的文件名
    file_name = os.path.basename(first_tmp_file)

    print(file_name)
    return f'python {file_name}'


# fake actions
CHOICES = ['panzhugui', 'availability', './exec_dispatch.sh', 'availability']


total_minutes = 0


def plus_total(total):
    global total_minutes
    total_minutes += total


def generate_time_slice(times):
    """
    生成 持续的时间片段
    :param times: 需要的片段数
    :return: array
    """
    total = 0
    time_slice = []
    for index in range(times):
        item = random.uniform(15, 30)
        time_slice.append(item)
        total += item
    plus_total(total)
    return time_slice


def generate_hold_segment(times, segments):
    """
    ① 根据times，生成 hold 时间片段
    ② 给每个时间片段， 增加 fake action
    :param times: 几次
    """
    times_slice = generate_time_slice(times)
    for index in times_slice:
        segments.append(f"sleep {index}m")
        segments.append("date")
        segments.append(random.choices(CHOICES)[0])


if __name__ == '__main__':

    print(sys.argv)
    # interval 时间，单位：小时
    hold_hours = int(sys.argv[1])

    direct_action = find_direct_action()
    segments = []
    # first, check script is work
    segments.append(direct_action)
    generate_hold_segment(hold_hours, segments)

    # finally, action
    segments.append(direct_action)
    final_command = ";".join(segments)

    print(final_command)
    print("-- hold position to: ", (datetime.datetime.now() + datetime.timedelta(minutes=total_minutes)).strftime("%Y-%m-%d %H:%M:%S"))

    pyperclip.copy(final_command)
    print("-- copied to clipboard!")
