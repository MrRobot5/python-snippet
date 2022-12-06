# -*- coding: utf-8 -*-
"""
    下载验证码图片

    参考： https://github.com/nladuo/USTBCrawlers/blob/master/lesson8/downloader/downloader.py
"""
import requests
import uuid
from PIL import Image
import os

url = "http://xjzw.th28.cn/default_pay_template/images/yzm.jsp?0.7855853862762292"
resp = requests.get(url)
filename = "/tmp/captchas/" + str(uuid.uuid4()) + ".bmp"
with open(filename, 'wb') as f:
    for chunk in resp.iter_content(chunk_size=1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
            f.flush()
    f.close()
im = Image.open(filename)
if im.size != (60, 20):
    os.remove(filename)
else:
    print(filename)

