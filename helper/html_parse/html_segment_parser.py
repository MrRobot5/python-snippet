# -*- coding:utf-8 -*-

"""
    功能： 从html 片段中，提取需要的信息。
    pip install beautifulsoup4

    字符串操作，文档： 5.Built-in Types -  5.6.Sequence Types — str, unicode, list, tuple, bytearray, buffer, xrange
    str.strip([chars])
"""
from bs4 import BeautifulSoup

import logging


def parse_script():
    html = open("../../html/iciba.html", "r", encoding='UTF-8')
    soup = BeautifulSoup(html.read(), 'html.parser')
    elements = soup.select('.btn')

    result = []
    for element in elements:
        print(element.text)
        result.append(get_attrs(element, "id") + element.text)

    print(result)


def get_attrs(element, attr):
    """
    判断attrs, 防止获取没有的key 报错。
    """
    if attr in element.attrs:
        return element.attrs[attr]
    else:
        return "--"


if __name__ == '__main__':
    parse_script()

