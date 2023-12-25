"""
从指定的URL获取分页接口数据，并在数据不为空时更新时间戳并重新请求。
以下是一个简化的代码示例，展示了如何实现这个过程

@author chat-gpt
@since 2023年12月25日 20:09:38
"""

import requests
from datetime import datetime, timedelta


# 函数用于获取数据并在数据不为空时更新时间戳
def fetch_data(timestamp):
    # 构建请求URL
    url = f"https://www.zhihu.com/api/question/queryNumberDecrypt?decryptFields=undefined&from={timestamp}"

    # 发送GET请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        data = response.json()

        # 如果数据不为空，则更新时间戳并递归调用函数
        if data:  # 根据实际返回数据结构判断是否为空
            # 减去140天
            new_timestamp = next_timestamp(timestamp)
            # 递归调用函数
            fetch_data(new_timestamp)
        else:
            print("No more data available.")
    else:
        print(f"Failed to fetch data, status code: {response.status_code}")


def next_timestamp(timestamp):
    """
    减去140天
    @param timestamp: start
    @return: start - 140
    """
    # utcfromtimestamp 将毫秒时间戳转换为datetime对象
    start_date = datetime.utcfromtimestamp(timestamp / 1000)
    new_date = start_date - timedelta(days=140)
    # 将datetime对象转换为毫秒时间戳
    new_timestamp = int(new_date.timestamp() * 1000)
    return new_timestamp


if __name__ == '__main__':
    # 初始时间戳
    initial_timestamp = datetime.now().timestamp()

    # 调用函数开始处理
    fetch_data(initial_timestamp)
