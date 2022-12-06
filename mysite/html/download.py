# -*- coding: UTF-8 -*-

"""
下载网页文件到本地文件夹
"""
import os, urllib2, urllib

path = "/tmp"
file_name = 'MSFT.csv'
dest_dir = os.path.join(path, file_name)

# 设置下载链接的路径
url = "http://gou.m.jd.com/"


# 定义下载函数downLoadPicFromURL（本地文件夹，网页URL）
def download_pic(dest_dir, url):
    try:
        urllib.urlretrieve(url, dest_dir)
    except IOError as e:
        print '\tError retrieving the URL: {}, for {}'.format(url,  e)


download_pic(dest_dir, url)
