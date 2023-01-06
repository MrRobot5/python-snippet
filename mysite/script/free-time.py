# -*- coding:utf-8 -*-
import sys
import random
import pyperclip
import datetime


# 假动作
CHOICES = ["./swagger-1.exe", "./swagger-calendar.exe", "./batch-exe.sh"]


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


def generate_hold_segment(times=1):
    """
    生成 hold 时间片段, 支持总时间的累加
    :param times: 几次
    :return:
    """
    times_slice = generate_time_slice(times)
    result = []
    for index in times_slice:
        result.append("sleep {}m".format(index))
        result.append("date")
        result.append("./menu.exe")
    return result


if __name__ == '__main__':
    """
        打击时间规划脚本，提供周末的随机打击记录
        整体思路：先保持唤醒一段时间，然后开始执行打击记录。打击记录间隔采用随机时间。
        关键参数：hold_hours click_hours
        会生成对应的两部分时间片段，合并为完整的执行命令 final_command
    """
    print(sys.argv)
    # 唤醒时间，单位：小时
    hold_hours = int(sys.argv[1])
    # 需要的打击时间间隔，单位：小时
    click_hours = int(sys.argv[2])

    segments = ["./prepare.exe"]
    segments += generate_hold_segment(hold_hours)
    # alias move='/e/export/jeff-info'
    segments.append("move")
    for i in range(click_hours):
        segments += random.choices(CHOICES)
        segments += generate_hold_segment()

    segments.append("move")
    final_command = ";".join(segments)
    pyperclip.copy(final_command)

    print(final_command)
    print("-- hold position to: ", (datetime.datetime.now() + datetime.timedelta(minutes=total_minutes)).strftime("%Y-%m-%d %H:%M:%S"))
    print("-- copied to clipboard!")
