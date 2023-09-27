import csv

"""
csv 文件转为 Insert SQL
使用场景： 批量数据导入，借助 csv 文件来生成 Insert SQL
@since 2023-08-15 11:36:19 chat-gpt
"""

table_name = 'your_table_name'  # replace with your table name


def csv_to_insert_sql(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # header row

        for row in reader:
            values = ['"' + value + '"' if value else '""' for value in row]
            sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(values)});"
            print(sql)


if __name__ == '__main__':
    # 用法示例
    csv_to_insert_sql("csv_sample.csv")
