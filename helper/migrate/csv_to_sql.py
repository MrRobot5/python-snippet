import csv

"""
csv 文件转为 Insert SQL
使用场景： 批量数据导入，借助 csv 文件来生成 Insert SQL
@since 2023-08-15 11:36:19 chat-gpt
"""

table_name = 'your_table_name'  # replace with your table name


def csv_to_insert_sql(csv_file):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # header row

        # 使用'a'模式打开文件，如果文件不存在，会自动创建
        with open('output.txt', 'a') as f:
            for row in reader:
                values = ['"' + value + '"' if value else '""' for value in row]
                sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(values)});"
                print(sql)
                # 写入 sql 字符串并添加换行符
                f.write(sql + '\n')


if __name__ == '__main__':
    # 用法示例
    csv_to_insert_sql("csv_sample.csv")
