"""
从指定的URL获取分页接口数据，并在数据不为空时更新时间戳并重新请求。
以下是一个简化的代码示例，展示了如何实现这个过程

@author chat-gpt
@since 2023年12月25日 20:09:38
"""

import requests
import pandas as pd
import sqlalchemy as sa
from sqlalchemy import create_engine
import time
from datetime import datetime, timedelta

#
symbol = 'SH601088'

headers = {
    'authority': 'stock.xueqiu.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'origin': 'https://xueqiu.com',
    'pragma': 'no-cache',
    'referer': f'https://xueqiu.com/S/{symbol}',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

session = requests.Session()
engine = create_engine(f"sqlite:///database_{symbol}.db", pool_recycle=3600, echo=True)

# 函数用于获取数据并在数据不为空时更新时间戳
def fetch_data(timestamp):
    # 构建请求URL
    url = f"https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={symbol}&begin={timestamp}&period=day&type=before&count=-142&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance"

    # 发送GET请求
    response = session.get(url, headers=headers)

    # 检查响应状态码
    response_data = response.json()["data"]
    
    # 如果数据不为空，则更新时间戳并递归调用函数
    if response_data:  # 根据实际返回数据结构判断是否为空
        c = response_data["column"]
        d = response_data["item"]
        data = pd.DataFrame(d, columns=c)
        data['timestamp'] = data['timestamp'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x / 1000)))
        # Write records stored in a DataFrame to a SQL database.
        # if_exists{‘fail’, ‘replace’, ‘append’}, default ‘fail’
        data.to_sql("kline_data", con=engine, if_exists="append")
        # sleep(seconds)
        time.sleep(1)

        # 减去140天
        new_timestamp = next_timestamp(timestamp)
        # 递归调用函数
        fetch_data(new_timestamp)
    else:
        print("No more data available.")
    


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
    session.get('https://xueqiu.com/?_=lqvl7ow8', headers=headers)
    # 初始时间戳
    initial_timestamp = datetime.now().timestamp()

    # 调用函数开始处理
    fetch_data(int(initial_timestamp * 1000))
