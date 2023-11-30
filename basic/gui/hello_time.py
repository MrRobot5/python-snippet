# encoding: utf-8

"""
点击脚本生成模版

https://pypi.org/project/opencv-python/

软件包依赖 pyautogui -> pyscreeze -> cv2 -> opencv

Q: Do I need to install also OpenCV separately?
A: No, the packages are special wheel binary packages and they already contain statically built OpenCV binaries.

@since 2023年11月27日15:36:33
"""

import time
import pyautogui

# 生成唯一的文件名
timestamp = time.strftime("%Y%m%d-%H%M%S")
filename = f"/export/temp-{timestamp}.py"

print("请输入文本（收藏实例）")

with open(filename, 'w') as file:
    file.write('import pyautogui \n')
    file.write('import random \n')
    file.write('offset = random.uniform(-50, 5) \n')
    image_location = pyautogui.locateOnScreen("Snipaste_2023-11-27_11-00-31.png", grayscale=True)
    position = pyautogui.center(image_location)
    print(position.x, position.y)
    # 通过本脚本的样本 location， 定位需要的 location
    file.write(f'pyautogui.moveTo({position.x - 60} + offset, {position.y} + offset, 2, pyautogui.easeOutQuad) \n')
    file.write('pyautogui.click() \n')

print(f"输入已保存到文件 {filename}")
