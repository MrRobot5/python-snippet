"""
在会话中保留状态，可以使用request.Session()
应用场景： 爬虫自动获取 cookie，复用到其他 http 请求中

@since 2023年12月25日 15:30:34
"""

import requests
import json

headers = {
    'authority': 'stock.xueqiu.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://xueqiu.com',
    'pragma': 'no-cache',
    'referer': 'https://xueqiu.com/S/SZ000625',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


# 获取cookie
response = requests.get('https://xueqiu.com/?_=lqvl7ow8', headers=headers)
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
