import csv
import threading
import requests
from concurrent.futures import ThreadPoolExecutor

"""
功能： 读取 csv 文件，获取远程数据，并处理为需要的数据。 
技术点：
    1. 使用线程池，并发处理。提高处理效率。
    2. 读写 csv 文件。更贴近实际使用。
@since: 2023-08-04 15:34:36 chat-gpt
"""

headers = {
    'app-token': 'noop',
    "accept": "*/*",
    "Content-Type": "application/json"
}

# 线程数
num_threads = 16

data = []


def process_line(line):
    # print(threading.current_thread())

    response = requests.get("http://c.foo.com/getsitePinInfo.json?erp=" + line, headers=headers)

    # 将API调用结果转换为csv格式并写入文件
    json = response.json()
    site = json.get("data")
    print("erp='{erp}', c2={siteDepart}, c3='{siteCode}'".format(**site))

    response = requests.get("http://c.foo.com/site/getsite?siteCode=" + line, headers=headers)
    json = response.json()
    site.update(json.get("data"))

    data.append(site)


if __name__ == '__main__':
    with open('C:/Users/yangpan3/Downloads/明细表_20230801150358.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        lines = [row['sales_erp'] for row in reader]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(process_line, lines)

    # 写入CSV文件
    with open('data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 写入CSV文件的表头
        writer.writerow(data[0].keys())

        # 写入每行数据
        for row in data:
            writer.writerow(row.values())
