# -*- coding: UTF-8 -*-

"""
cookie 模拟登录请求html
登录知乎后，打开burpsuit，刷新知乎页面获取cookie，并将cookie保存到本地

pip install requests

https://www.jianshu.com/p/c94de9f1ef7c requests读取本地cookie实现模拟登录

https://blog.csdn.net/dnxbjyj/article/details/70254428 requests和BeautifulSoup库的基本用法

"""
import requests
from bs4 import BeautifulSoup


def get_cookie():
    """
    将cookie 文件转换成字典形式
    :return:
    """
    with open('cookie.txt', 'r') as f:
        cookies = {}
        for line in f.read().split(';'):
            # 1代表只分割一次
            name, value = line.strip().split('=', 1)
            cookies[name] = value
        return cookies


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.zhihu.com/'
}


def fetch_html():
    session = requests.Session()
    url = 'http://www.zhihu.com/app/group/toConfigPage/75718'

    response = session.post(url, data={"appId": 30099, "editFlag": True, "envType": "PRODUCTION"}, headers=headers,
                            cookies=get_cookie(), verify=False)
    html = response.content

    # 将获取到的页面源码写入zhihu.html文件中
    with open('zhihu.html', 'w') as f:
        f.write(html)

    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    # 获取自定义属性值
    alink = soup.select("a[name='a_group_hisBtn']")
    for link in alink:
        print(link["data-key"])


if __name__ == '__main__':
    # fetch_jone_html()
    # fetch_jone_file()
    result = get_cookie()
    print(result)