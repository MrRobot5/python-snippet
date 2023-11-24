# encoding: utf-8

"""
解析你的Java代码并生成CSV文件。

首先，使用private关键字来分割代码块，这样每个块都包含一个字段的注释和定义。
然后，我们按照之前的方法处理每个块，提取注释、字段类型和字段名称，并将它们写入CSV文件。
@since 2023年11月23日20:22:45 chat-gpt
"""

import csv

# 你的Java代码
java_code = """

    /**
     * 签署方类型: 
     * 2大陆企业，3个体工商户
     */
    private Integer clientType;

    /**
     * 证件号/签署方统一社会信用代码
     */
    private String certificateCode;

    /**
     * 签约人姓名
     */
    private String signUserName;
    
"""

# 初始化blocks列表和临时block字符串
blocks = []
block = ""

# 遍历每一行
for line in java_code.splitlines():
    if line.strip().startswith('private'):
        block += line + '\n'
        blocks.append(block)
        block = ''  # 开始新的block
    else:
        block += line + '\n'  # 将行添加到当前block

# 创建CSV文件
with open('output.csv', 'w', newline='', encoding='gbk') as file:
    writer = csv.writer(file)
    writer.writerow(["字段类型", "字段名称", "字段代码注释文字"])  # 写入标题
    for block in blocks:
        # 分割注释和字段定义
        parts = block.strip().split('\n')
        comment = ' '.join(part.strip(' *') for part in parts if part.strip().startswith('*'))
        field_line = parts[-1].strip()
        field_parts = field_line.split(" ")
        field_type = field_parts[1]
        field_name = field_parts[2].rstrip(';')
        writer.writerow([field_type, field_name, comment])  # 写入数据
