
"""
csv 数据生成格式转化后的 insert sql
@since 2023年12月5日20:19:36 chat-gpt
"""

import csv
import requests

# 类型到customer_type的映射
type_mapping = {
    "个人": 1,
    "企业": 2,
    "个体工商户": 3,
    "国家机构": 4,
    "境外": 5,
    "港澳台": 6
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': '',  # 请替换为实际的Cookie值
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_customer_code(param1, param2, param3):
    """
    从远程 Http 接口获取编码数据
    @param param1:
    @param param2:
    @param param3:
    @return:
    """
    data = {
        'certificateCode': param1,
        'certificateType': 2,
        'customerName': param2,
        'customerType': param3
    }

    response = requests.post("http://admin-pre.foo.com/api/customer/createByAuth", headers=headers, json=data, verify=False)

    print(response.json())
    return response.json()["data"]


# 创建SQL语句
sql_statements = []

with open("C:/Users/yangpan3/Downloads/初始内部主体维护.csv", 'r') as file:
    reader = csv.reader(file)
    next(reader)  # skip header row ✔
    for row in reader:
        customer_type = type_mapping.get(row[0], "NULL")  # 如果类型不在映射中，使用NULL
        customer_code =  get_customer_code(row[2], row[1], customer_type)
        sql = f"INSERT INTO `foo_customer` (`customer_name`, `customer_code`, `certificate_code`, `customer_type`, `country_code`, `create_user`) VALUES ('{row[1]}', '{customer_code}', '{row[2]}', {customer_type}, '{row[3]}', 'system');"
        sql_statements.append(sql)

# 打印SQL语句
for sql in sql_statements:
    print(sql)