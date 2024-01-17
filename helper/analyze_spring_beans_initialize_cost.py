"""
prompt: 使用 Python 提取log 文件中含有 initialized in 关键字的行，并且解析文本，
参考 initialized in 284 ms 格式，提取其中的数字，并且按照数字大小降序输出

使用场景： 分析Spring 启动日志， 找出初始化耗时长的Bean

@since 2024年1月17日 17:38:39 chat-gpt
"""

import re

# 日志文件路径
log_file_path = 'crm_project_management_all.log'

# 用于存储解析出的数字和对应的行文本
initialization_data = []

# 正则表达式匹配 "initialized in" 后面的数字。 配合 TimingBeanPostProcessor 一起使用。
pattern = re.compile(r'initialized in (\d+) ms')

# 读取并处理日志文件
with open(log_file_path, 'r', encoding='UTF-8') as file:
    for line in file:
        if 'initialized in' in line:
            match = pattern.search(line)
            if match:
                # 将匹配到的数字转换为整数并与行文本一起添加到列表中
                initialization_data.append((int(match.group(1)), line.strip()))

# 按数字大小降序排序
initialization_data.sort(key=lambda x: x[0], reverse=True)

# 输出结果
for time, text in initialization_data:
    print(f"{time} ms - {text}")
