python lab
====

## sqlparse

> sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements.

`pip install sqlparse`



pip install pyperclip

> > > import pyperclip
> > > pyperclip.copy('The text to be copied to the clipboard.')
> > > pyperclip.paste()
> > > 'The text to be copied to the clipboard.'

## PyAutoGUI

> PyAutoGUI lets your Python scripts control the mouse and keyboard to automate interactions with other applications. 

To install with pip, run: `pip install pyautogui`

```shell
>>> import pyautogui

>>> screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

>>> currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

>>> pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

>>> pyautogui.click()          # Click the mouse.
>>> pyautogui.click(100, 200)  # Move the mouse to XY coordinates and click it.
>>> pyautogui.click('button.png') # Find where button.png appears on the screen and click it.

>>> pyautogui.move(0, 10)      # Move mouse 10 pixels down from its current position.
>>> pyautogui.doubleClick()    # Double click the mouse.
>>> pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

>>> pyautogui.write('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
>>> pyautogui.press('esc')     # Press the Esc key. All key names are in pyautogui.KEY_NAMES

>>> pyautogui.keyDown('shift') # Press the Shift key down and hold it.
>>> pyautogui.press(['left', 'left', 'left', 'left']) # Press the left arrow key 4 times.
>>> pyautogui.keyUp('shift')   # Let go of the Shift key.

>>> pyautogui.hotkey('ctrl', 'c') # Press the Ctrl-C hotkey combination.

>>> pyautogui.alert('This is the message to display.') # Make an alert box appear and pause the program until OK is clicked.
```

## Redis in Action 笔记

### installing.py 作用

Fetch a module that will help you install other packages

Redis client library install
python -m easy_install redis

Testing Redis from Python

Installing Redis on Windows
https://github.com/dmajkic/redis/downloads

By  reading  this  book,  you  can  learn  about  many  of  the  tips,  tricks,  and  well-known problems that have been solved using Redis。

for most databases, inserting rows is a very fast operation (inserts write to the end of an on-disk
file, not unlike Redis’s append-only log). But updating an existing row in a table is fairly
slow (it can cause a random read and may cause a random write)

STRINGs,  LISTs,  SETs,  HASHes, and ZSETs.

described  in  appendix  A,  you  should  also  have  installed  Python  and  the  necessary
libraries to use Redis from Python as part of that process.

Web requests in this type of situation are considered to be stateless in that the web servers themselves don’t  hold  information  about  past  requests,  in  an  attempt  to  allow  for  easy  replace -ment of failed servers.

资源：
http://dev.maxmind.com/geoip/legacy/geolite/
http://www.hostip.info/dl/

参考：
http://redis.io/commands

可视化插件：
https://d3js.org/
http://graphite.wikidot.com/

## urllib和request的区别总结

request
使用的是 urllib3，继承了urllib2的所有特性。Requests支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动确定响应内容的编码，支持国际化的 URL 和 POST 数据自动编码。
