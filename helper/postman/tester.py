# encoding: utf-8

"""
批量发起 http 请求。
@see batch_task.py 类似功能
@since 2023-05-06 15:02:01
"""

import requests

headers = {
    'lop-pin': 'foo',
    'LOP-DN': '*/*',
    'accept': '*/*',
    'Content-Type': 'application/json',
}


def get_source_data(param):
    data = {'pin': param}
    response = requests.get("http://s.foo.com/getUserPinInfo.json", headers=headers, params=data)
    print(response.json())


if __name__ == '__main__':
    lines = open('source.txt', "r").readlines()
    for line in lines:
        get_source_data(line.strip())
