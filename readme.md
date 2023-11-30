# python 工具库

---

# 👉规范

①**basic**  python 基础功能和依赖库的使用示例、代码片段

②**helper** 实践工具，有具体的使用场景



# ⚔helper

| NO  | 文件                     | 功能         | 备注                  |
| --- | ---------------------- | ---------- | ------------------- |
| 1   | batch_task.py          | 批量请求关键信息   | 从 http api 快速获取信息   |
| 2   | soso_pic_downloader.py | 爬取斗鱼相册     | json 解析，文件下载        |
| 3   | html_segment_parser.py | html 解析    | 快速提取html 片段，得到需要的信息 |
| 4   | guess_my_crab_code.py  | 尝试匹配正确的提取码 | 验证码识别、网络请求提交、日志文件   |
| 5   | example.py             | 词云         |                     |

# 🔨wheel

## sqlparse

> sqlparse is a non-validating SQL parser for Python. It provides support for parsing, splitting and formatting SQL statements.

`pip install sqlparse`

## beautifulsoup4

`pip install beautifulsoup4`

## 剪贴板

`pip install pyperclip`

> import pyperclip
> pyperclip.copy('The text to be copied to the clipboard.')
> pyperclip.paste()
> 'The text to be copied to the clipboard.'

## PyAutoGUI

> PyAutoGUI lets your Python scripts control the mouse and keyboard to automate interactions with other applications. 

To install with pip, run: `pip install pyautogui`

```shell
import pyautogui

screenWidth, screenHeight = pyautogui.size() # Get the size of the primary monitor.

currentMouseX, currentMouseY = pyautogui.position() # Get the XY position of the mouse.

pyautogui.moveTo(100, 150) # Move the mouse to XY coordinates.

pyautogui.click()          # Click the mouse.
pyautogui.click(100, 200)  # Move the mouse to XY coordinates and click it.
pyautogui.click('button.png') # Find where button.png appears on the screen and click it.

pyautogui.move(0, 10)      # Move mouse 10 pixels down from its current position.
pyautogui.doubleClick()    # Double click the mouse.
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad)  # Use tweening/easing function to move mouse over 2 seconds.

pyautogui.write('Hello world!', interval=0.25)  # type with quarter-second pause in between each key
pyautogui.press('esc')     # Press the Esc key. All key names are in pyautogui.KEY_NAMES

pyautogui.keyDown('shift') # Press the Shift key down and hold it.
pyautogui.press(['left', 'left', 'left', 'left']) # Press the left arrow key 4 times.
pyautogui.keyUp('shift')   # Let go of the Shift key.

pyautogui.hotkey('ctrl', 'c') # Press the Ctrl-C hotkey combination.

pyautogui.alert('This is the message to display.') # Make an alert box appear and pause the program until OK is clicked.
```

## Redis

`pip install redis`

### 资源：

参考：
http://redis.io/commands

可视化插件：
https://d3js.org/
http://graphite.wikidot.com/

## urllib和request的区别总结

request 使用的是 urllib3，继承了urllib2的所有特性。Requests支持HTTP连接保持和连接池，支持使用cookie保持会话，支持文件上传，支持自动确定响应内容的编码，支持国际化的 URL 和 POST 数据自动编码。

> There are many libraries to make an HTTP request in Python, which are [httplib](https://docs.python.org/2/library/httplib.html), [urllib](https://docs.python.org/2/library/urllib.html), [httplib2](https://github.com/httplib2/httplib2), [treq](https://github.com/twisted/treq), etc., but [requests](https://2.python-requests.org//en/master/) is the one of the best with cool features.
