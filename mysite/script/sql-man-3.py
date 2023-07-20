
"""
根据提供的基础数据，生成 sql 脚本。 使用 gpt 生成。
@since 2023-07-20 20:58:06
"""

data = [
    ['tommy', '太原'],
    ['alice', '晋阳'],
    # ... rest of the data
]

mapping = {
    '太原': 597,
    '晋阳': 598
}

if __name__ == '__main__':
    for row in data:
        erp = row[0]
        department = row[1]
        departmentId = mapping.get(department)

        sql_statement = f"UPDATE table SET region_id = 423, battle_id = {departmentId} WHERE erp = '{erp}';"
        print(sql_statement)
