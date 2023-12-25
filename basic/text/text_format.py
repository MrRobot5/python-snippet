"""
文本段落提取、格式化数据
使用场景： 从给定的文本段落中，提取 csv 格式数据

prompt:
使用python 格式化数据，示例：
业务编号：FA2312010001112
手机号从11111221115改为11111750003

业务编号：FA2312010001249
手机号从11111221115改为11111750003
需求是：提取业务编号：作为第一列， 提取改为后续的手机号作为第二列
@since 2023年12月11日17:34:22 chat-gpt

"""

import re

# 示例数据
data = """
业务编号：FA2312010001112
balabla
手机号从11111221115改为11111750003

业务编号：FA2312010001249
手机号从11111221115改为11111750003
"""

# 分割数据为段落
entries = data.strip().split('\n\n')

# 遍历每个段落
for entry in entries:
    # 使用正则表达式提取业务编号(以 FA 开头的单词)和手机号(最后的 11 个数字)
    contract_number = re.search(r'(FA\d+)', entry)
    new_number = re.search(r'(\d{11}$)', entry)

    # 如果找到了业务编号和新编号
    if contract_number and new_number:
        # 输出格式化的数据
        print(f'{contract_number.group(1)} \t {new_number.group(1)}')
    else:
        # 不符合的也要打印出来，防止遗漏
        print(entry)
