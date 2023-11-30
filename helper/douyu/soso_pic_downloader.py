# -*- coding:utf-8 -*-

import json
import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://yuba.douyu.com/'
}


# 测试--结果json 数据结构解析
def load_json():
    f = open("Y578lG8pB7EM.json", "r", encoding='UTF-8')
    result = json.load(f)

    for month in result["data"]:
        print("current month is : {}".format(month["month"].encode('utf-8')))
        pics = month["list"]
        for pic in pics:
            print(pic["src"])


def download(pic_src):
    session = requests.Session()
    response = session.get(pic_src, headers=headers, timeout=50)
    filename = str(pic_src).split("?")[0].split("/")[-1]
    print('--filename:[{}] download success'.format(filename))
    f = open("soso/{}".format(filename), "wb")
    f.write(response.content)
    f.close()


def download_pic_list(file_path):
    print("current file_path is : {}".format(file_path))
    f = open(file_path, "r", encoding='UTF-8')
    result = json.load(f)

    for month in result["data"]:
        print("current month is : {}".format(month["month"].encode('utf-8')))
        pics = month["list"]
        for pic in pics:
            download(pic["src"])


# 根据分页规律，获取下一个分页id
def get_next_feed_id(content):
    result = json.loads(content)
    if len(result["data"]) == 0:
        print("抓取结束！")
        return ""

    last_month = result["data"][-1]
    last_pic = last_month["list"][-1]
    next_feed_id = last_pic["feed_id_str"]
    print(next_feed_id)
    return next_feed_id


# 获取图片路径集合json
def fetch_json(json_url, current_feed_id):
    session = requests.Session()
    response = session.get(json_url, headers=headers, timeout=50)
    print('--url:[{}] download success'.format(json_url))
    f = open("douyu-pics-{}.txt".format(current_feed_id), "wb")
    f.write(response.content)
    f.close()

    return get_next_feed_id(response.content)


# 首先按照顺序抓取图片分页的json
def step_1():
    feed_id = fetch_json("https://yuba.douyu.com/wbapi/web/user/album/rEdlX6oeYdNM?timestamp=0.38067080966479794", "0")
    while len(feed_id) > 0:
        page_url = "https://yuba.douyu.com/wbapi/web/user/album/rEdlX6oeYdNM?offset=1&feed_id={}&timestamp=0.041190611968733526".format(
            feed_id)
        feed_id = fetch_json(page_url, feed_id)


# 然后根据得到的json 下载图片
def step_2():
    for filename in os.listdir('/tmp/foo/douyu/'):
        # print filename
        if filename.endswith('txt'):
            download_pic_list('/tmp/foo/douyu/{}'.format(filename))


# step_1 分页获取图片路径集合
# step_2 下载图片集合
if __name__ == '__main__':
    load_json()
    # step_1()
    step_2()
