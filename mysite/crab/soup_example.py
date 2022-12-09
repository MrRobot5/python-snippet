# -*- coding:utf-8 -*-

"""
    pip install beautifulsoup4

    字符串操作，文档： 5.Built-in Types -  5.6.Sequence Types — str, unicode, list, tuple, bytearray, buffer, xrange
    str.strip([chars])
"""
from bs4 import BeautifulSoup

import logging


def parse_script():
    html = open("iciba.html", "r", encoding='UTF-8')
    soup = BeautifulSoup(html.read(), 'html.parser', from_encoding='UTF-8')
    img = soup.select('img')[0]
    result = img.attrs['src']
    print(result.strip())


if __name__ == '__main__':
    parse_script()

