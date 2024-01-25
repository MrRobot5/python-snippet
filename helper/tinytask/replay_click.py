"""
prompt: 使用python 从日志文件中读取每一行日志，根据“2024-01-25 21:36:35,321: Mouse clicked at (1405, 1171) with Button.left” ，解析其中的坐标(1405, 1171) 和 Button.left ， 用pyautogui 按照解析的坐标和左右键，重放鼠标点击
读取日志文件，解析坐标和鼠标按钮，然后使用pyautogui来模拟点击
此脚本会读取日志文件的每一行，使用正则表达式来查找匹配的日志条目，并提取坐标和按钮信息，然后使用pyautogui来模拟鼠标点击。

@since 2024年1月25日 22:07:25 chat-gpt
"""

import re
import pyautogui
import time

# 正则表达式用于匹配日志中的坐标和按钮
log_pattern = re.compile(r"Mouse clicked at \((\d+), (\d+)\) with (Button\.\w+)")

# 读取日志文件并解析每一行
with open('mouse_log.txt', 'r') as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            # 提取坐标和按钮
            x, y = int(match.group(1)), int(match.group(2))
            button = match.group(3).split('.')[1].lower()  # 'Button.left' -> 'left'

            # 模拟鼠标点击
            pyautogui.click(x=x, y=y, button=button)

            # 可以在点击之间添加延时
            time.sleep(0.5)  # 100毫秒的延时
