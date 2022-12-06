# -*- coding:utf-8 -*-

"""
    pip install beautifulsoup4

    字符串操作，文档： 5.Built-in Types -  5.6.Sequence Types — str, unicode, list, tuple, bytearray, buffer, xrange
    str.strip([chars])
"""
from bs4 import BeautifulSoup
import time
import logging

def parse_script():
    sample = open("/tmp/line.txt", "r")
    soup = BeautifulSoup(sample.read(), 'html.parser', from_encoding='utf-8')
    script = soup('script')[5]
    result = script.get_text().split(";")[0]
    print result.strip()

    message = result.encode('gb2312').strip()
    if message.find("无效提货编码") > -1:
        logging.info("{0} {1} = {2}".format(1, 2, message))
    else:
        logging.warning("code {0} {1} = {2}".format(1, 2, message))


def range_test():
    for i in range(10000, 20000):
        print str(i) + "s"
        time.sleep(0.1)


parse_script()


