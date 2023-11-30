# encoding: utf-8

"""
pip install pyautogui

"""
import pyautogui

screenWidth, screenHeight = pyautogui.size()
pyautogui.moveTo(77, 195)
pyautogui.click()
pyautogui.write('Hello world!', interval=0.25)
pyautogui.hotkey('alt', 'a')
pyautogui.screenshot()
