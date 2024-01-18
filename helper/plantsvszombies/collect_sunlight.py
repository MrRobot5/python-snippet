
"""
根据快捷键自动收集 sunlight
你可以使用 keyboard 库来监听快捷键，以及 webbrowser 库来打开浏览器。
使用pyautogui库识别屏幕上多个相同的图标并遍历点击它们

pyautogui.PAUSE = 0.25  # 设置每个操作后的暂停时间为0.25秒

pip install keyboard

@since 2024年1月18日 16:45:30
"""

import keyboard
import pyautogui
import time

# 首先，确保你有一个图标的截图，这个截图将用于匹配屏幕上的图标
icon_path = 'icon.png'

def collect_sunlight():
    # 使用pyautogui.locateAllOnScreen函数查找屏幕上所有匹配的图标
    for pos in pyautogui.locateAllOnScreen(icon_path, confidence=0.9):  # confidence参数可以调整匹配的准确度
        # 获取图标中心的坐标
        center_x, center_y = pyautogui.center(pos)

        # 移动鼠标到图标位置并点击
        pyautogui.click(center_x, center_y)

        # 等待一段时间，以便应用程序响应点击（如果需要）
        time.sleep(0.1)

if __name__ == '__main__':
    # 设置快捷键为 'ctrl+shift+b'
    keyboard.add_hotkey('ctrl+shift+b', collect_sunlight)

    # 保持程序运行，直到用户按下esc键
    keyboard.wait('esc')


