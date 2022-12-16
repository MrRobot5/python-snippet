# encoding: utf-8

"""
批量获取任务详情信息，快速获取关注的信息

2022年12月09日 15:54:49
"""

import requests
import jsonpath

# 需要请求的 url pattern
REQUEST_API = 'http://example.foo.com/api/oe/ticket/{}'

cookies = {
    'mba_muid': '16685236794961410676977',
    '登录cookie_name': '3620221216142312',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}


def get_json(param):
    """
    请求 Http 接口，获取Json 数据
    :param param: 任务id
    :return: ['yangpan23']
    """
    response = requests.get(REQUEST_API.format(param), cookies=cookies, headers=headers, verify=False)
    # response.json() returns a JSON object of the result
    json = response.json()

    output = jsonpath.jsonpath(json, '$.data.assignee')
    return output


def read_lines():
    """
    打开当前目录下的 input.txt， 读取文件行
    :return: ['line']
    """
    original = open('input.txt', "r")
    lines = original.readlines()
    return lines


if __name__ == '__main__':
    # 1.source
    source = read_lines()
    # 2.loop and handle
    for line in source:
        # strip() with leading and trailing whitespace removed.
        print("{} {}".format(line.strip(), get_json(line)[0]))


