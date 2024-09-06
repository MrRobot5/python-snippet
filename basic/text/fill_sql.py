
"""
功能：填充 mybatis 打印的SQL。
prompt:
    从文件读取两行内容。
    提取Preparing as sql 和 Parameters。按照占位符？顺序，把参数Parameters填充进去 sql, 输出完整sql 字符串。
    例如：
    Preparing: insert into foo ( id, finish, fd_time, create_time, update_time, yn ) values ( ?, ?, now(), now(), now(), 1 )
    Parameters: 21744506(Integer), 1(Integer)
@since 2024年7月17日 14:41:33 chat-gpt
"""


def fill_sql_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # 读取文件中的两行内容
        preparing = file.readline().strip()
        parameters = file.readline().strip()

    # 提取 SQL 语句
    sql = preparing.split("Preparing: ")[1].strip()

    # 提取参数
    params = parameters.split("Parameters: ")[1].strip()

    # 将参数解析成列表
    param_list = []
    for param in params.split(", "):
        if '(' in param:
            value, dtype = param.split("(")
            dtype = dtype.rstrip(")")
            if dtype == "Integer" or dtype == "Double" or dtype == "Byte" or dtype == "BigDecimal" or dtype == "Long":
                param_list.append(value)
            elif dtype == "String" or dtype == "Timestamp":
                param_list.append(f"'{value}'")
        else:
            # 处理没有括号的情况，例如 null
            if param.lower() == "null":
                param_list.append("null")
            else:
                param_list.append(param)

    # 填充参数到 SQL 语句中
    for param in param_list:
        sql = sql.replace("?", param, 1)

    return sql


# 输入文件路径
if __name__ == '__main__':
    file_path = 'input.txt'
    # 输出完整的 SQL 语句
    filled_sql = fill_sql_from_file(file_path)
    print(filled_sql)

