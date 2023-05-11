# encoding: utf-8

"""
批量刷新线上数据。
@see batch_task.py 类似功能
@since 2023-05-06 15:02:01
"""

import requests
import json

headers = {
    'lop-pin': 'dazhanghong',
    'LOP-DN': '*/*',
    'accept': '*/*',
    'Content-Type': 'application/json',
}


def get_source_data(param):
    """
    加载远程数据。
    """
    data = {'messageId': param}
    response = requests.get("http://a.foo.com/common/message/getDetailById", headers=headers, params=data)
    return response.json()


def load_meta_data():
    """
    加载本地文件配置。 dict 结构
    usage: json_data.get("key")
    """
    file = open("FeHelper-20230506152326.json", "r", encoding='UTF-8')
    return json.load(file)


meta = load_meta_data()


def update(site):
    """
    发起数据 update SQL
    @param site: json 格式
    """
    data = "UPDATE foo SET c1='{c1}', c2={c2}, c3='{c3}' WHERE id={id};".format(**site)
    # data.encode() 解决包含中文字符串的问题
    response = requests.post('http://c.foo.com/api/v1/update/sql/1', headers=headers, data=data.encode())
    print(response.json())


def run(param):
    source = get_source_data(param)
    data = source["data"]
    # 不符合业务需要的数据， skip
    if not data.get("messageCode"):
        return

    siteName = meta.get(data.get("siteCode"))
    variable = json.loads(data.get("variable").replace('\n', ''))
    extend = {"siteName": siteName, "foo": param}
    # json 数据追加信息
    variable.update(extend)
    # 通过字典设置参数
    site = {"c1": param, "c2": siteName, "c3": json.dumps(variable, ensure_ascii=False).encode("utf8").decode(), "id": param}
    print(site)
    update(site)


if __name__ == '__main__':
    # 线上数据量比较大，根据id 逆向遍历
    for i in range(1907714, -1, -1):
        print(i)
        run(i)
    # get_source_data(400282)
    # load_meta_data()
