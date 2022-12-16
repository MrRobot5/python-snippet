# -*- coding: utf-8 -*-
"""
    下载验证码图片
    依赖 pip install Pillow
    参考： https://github.com/nladuo/USTBCrawlers/blob/master/lesson8/downloader/downloader.py
"""
import requests
import uuid
from PIL import Image
import os

EXAMPLE = "http://xjzw.th28.cn/default_pay_template/images/yzm.jsp?0.7855853862762292"


def download_image(url):
    resp = requests.get(url)
    filename = str(uuid.uuid4()) + ".bmp"
    with open(filename, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    image = Image.open(filename)
    if image.size != (60, 20):
        os.remove(filename)
    else:
        print(filename)


if __name__ == '__main__':
    download_image(EXAMPLE)


