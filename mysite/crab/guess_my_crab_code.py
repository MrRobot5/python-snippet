# -*- coding:utf-8 -*-

"""
    主程序，尝试匹配正确的提取码
    已知：部分提取码和密码
    需要重复尝试，猜出正确的提取码

    实现思路参考：http://www.cnblogs.com/hearzeus/p/5166299.html

    pip install requests
    pip install BeautifulSoup4

"""

import urllib
import urllib2
import cookielib
from PIL import Image
import cStringIO
from bs4 import BeautifulSoup
import pytesseract
import time
import logging.config


def init():
    logging.config.fileConfig("logging.conf")

    # 设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)


def parse_verify_code():
    # 下载验证码并存储cookie
    request = urllib2.Request("http://xjzw.th28.cn/default_pay_template/images/yzm.jsp?0.7855853862762292")
    request.add_header("Referer", "http://xjzw.th28.cn/codeinfoAction!verifyInit")
    resource = urllib2.urlopen(request).read()
    image = Image.open(cStringIO.StringIO(resource))
    # 人工识别 参考 parse_code.py
    # image.show()
    # code = raw_input("请输入验证码：")

    # ocr库识别
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    code = pytesseract.image_to_string(image)
    return code


def post_request(code, checkcode):
    req = urllib2.Request("http://xjzw.th28.cn/codeinfoAction!verifygc", urllib.urlencode(
        {"code": code, "password": "519559", "checkcode": checkcode, "verifytype": "0"}))
    response = urllib2.urlopen(req).read()

    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
    script = soup('script')[5]
    result = script.get_text().split(";")[0]

    # 打印结果
    logger = logging.getLogger("example01")
    logger.info("{0} {1}".format(code, checkcode))
    logger.info(result.strip())


def run():
    # 初始化环境
    init()
    # 遍历，拼接提货编码，请求server
    for i in range(4400, 8000):
        code = str(i) + "058529819725"

        checkcode = parse_verify_code()
        if len(checkcode) != 4:
            checkcode = parse_verify_code()

        try:
            post_request(code, checkcode)
        except:
            print "post error, retry!"
            try:
                post_request(code, checkcode)
            except:
                print "post error again!"

        time.sleep(0.1)


if __name__ == '__main__':
    run()

