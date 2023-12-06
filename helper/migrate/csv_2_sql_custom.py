
"""
csv 数据生成格式转化后的 insert sql
@since 2023年12月5日20:19:36 chat-gpt
"""

import csv

# 类型到customer_type的映射
type_mapping = {
    "个人": 1,
    "企业": 2,
    "个体工商户": 3,
    "国家机构": 4,
    "境外": 5,
    "港澳台": 6
}

# 创建SQL语句
sql_statements = []

with open("C:/Users/yangpan3/Downloads/初始内部主体维护.csv", 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # header row
    for row in reader:
        customer_type = type_mapping.get(row[0], "NULL")  # 如果类型不在映射中，使用NULL
        sql = f"INSERT INTO `foo_customer` (`customer_name`, `certificate_code`, `customer_type`, `country_code`, `create_user`) VALUES ('{row[1]}', '{row[2]}', {customer_type}, '{row[3]}', 'system');"
        sql_statements.append(sql)

# 打印SQL语句
for sql in sql_statements:
    print(sql)