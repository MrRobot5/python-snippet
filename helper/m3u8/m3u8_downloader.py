# -*- coding:utf-8 -*-

"""

在windows系统下面，直接可以使用:copy/b *.ts video.mp4  把所有ts文件合成一个mp4格式文件

参考：
python下载ts视频文件  https://blog.csdn.net/Lingdongtianxia/article/details/82886925
"""

import requests
import os
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
import time


def mission(url, index):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }

    print('--index:[{}] download start'.format(index))
    response = session.get(url, headers=headers, timeout=50)
    print('--index:[{}] download success'.format(index))
    f = open("/tmp/foo/m3u8-{}/%03d.ts".format(download_path) % index, "wb")
    f.write(response.content)
    f.close()
    print('--index:[{}] save success'.format(index))


download_path = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def check_dir():
    path = "/tmp/foo/m3u8-{}".format(download_path)
    if not os.path.exists(path):
        os.mkdir(path)
        print('--create dir:[{}]'.format(path))


if __name__ == "__main__":
    check_dir()
    pool = Pool(20)
    for n in range(1, 3):
        url = "https://f1.media.brightcove.com/1/1362235890001/5796758914001/1362235890001_5796758914001_s-{}.ts?pubId=1362235890001&videoId=1655020599001".format(
            n)
        pool.apply_async(mission, (url, n))
    pool.close()
    pool.join()
