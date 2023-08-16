# coding:utf-8

import json
from datetime import datetime

data_array = [
    {
        "snippet": "\n<input type=\"checkbox\" />io exception 回滚案例\n<input type=\"checkbox\" />大量数据更新案例",
        "modifyDate": 1638784454553,
        "colorId": 0,
        "subject": "",
        "alertDate": 0,
        "type": "note",
        "folderId": 0,
        "setting": {
            "themeId": 0,
            "stickyTime": 0,
            "version": 0
        },
        "id": "11570075234222336",
        "tag": "31981063419609152",
        "createDate": 1483059342142,
        "status": "normal",
        "extraInfo": "{\"title\":\"2016年12月30日\"}"
    }
]

table_name = "notes"

columns = ', '.join(data_array[0].keys())
values = ', '.join(['%s'] * len(data_array[0]))

insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

values_list = []


def date_format(date_):
    """
    chat-gpt
    如果您的日期字符串 "164***09" 表示的是以毫秒为单位的时间戳，您可以使用Python的datetime模块和timedelta类来将其转换为日期格式。以下是一个示例：
    @param date_ 它是以毫秒为单位的时间戳。
    @rtype: object
    """
    # 将毫秒转换为datetime对象
    date = datetime.fromtimestamp(date_ / 1000)
    # 格式化日期为"%Y-%m-%d"格式
    formatted_date = date.strftime("%Y-%m-%d")
    return formatted_date


for data in data_array:
    if 'setting' in data:
        # 删除 dict 属性
        del data['setting']

    item = {'id': data['id'], 'folderId': data['folderId'], 'content': data['snippet'], 'createdTime': date_format(data['createDate']), 'modifiedTime': date_format(data['modifyDate'])}

    values_list.append(tuple(item.values()))


if __name__ == '__main__':
    print(insert_query)
    print(values_list)
