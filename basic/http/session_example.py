"""
在会话中保留状态，可以使用request.Session()
应用场景： 爬虫自动获取 cookie，复用到其他 http 请求中

@since 2023年12月25日 15:30:34
"""

import requests
import json

# 获取cookie
response = requests.get('https://cn.bing.com/search?q=requests')
# 注意： requests.cookies 是一个RequestsCookieJar类
session_cookie = response.cookies

# 将CookieJar转为字典：
cookie_dict= requests.utils.dict_from_cookiejar(session_cookie)
with open("cookie_json.log", "w") as f:
    f.write(json.dumps(cookie_dict))

# 将字典转为CookieJar：
with open("cookie_json.log", "r") as f:
    load_cookies=json.loads(f.read())
    session_cookie = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)

# 其中cookie_dict是要转换字典
# 转换完之后就可以把它赋给cookies 并传入到session中了：
s = requests.Session()
s.cookies = session_cookie
