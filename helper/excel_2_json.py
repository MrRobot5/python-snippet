import pandas as pd

"""

这个脚本首先读取Excel数据，然后遍历每一行。
对于每一行，它首先查找一级原因是否已经存在于结果中。如果不存在，它将创建一个新的一级原因并添加到结果中。
然后，它在一级原因的子项中查找二级原因，如果不存在，它将创建一个新的二级原因并添加到一级原因的子项中。
最后，它创建一个新的三级原因并添加到二级原因的子项中。
在每一步中，它都会检查配置数据，如果找到匹配的标签，它将使用配置数据的键作为值，否则，它将使用计数器的当前值。

组件引用：
 pip install openpyxl
 pip install xlrd

@since: 2023-9-18 10:45:41 chat-gpt
"""

# 读取配置数据
config_data = [
    {"key": "100108", "value": "服务态度差"},
    {"key": "1002", "value": "价格原因"},
    # ... 其他配置数据
]

# 将配置数据转换为字典，方便查找
config_dict = {item['value']: item['key'] for item in config_data}


if __name__ == '__main__':
    # 读取Excel数据
    df = pd.read_excel('input.xlsx')

    # 初始化结果
    result = []

    # 初始化计数器
    counter = {"first": 20, "second": 2000, "third": 200000}

    # 遍历每一行数据
    for _, row in df.iterrows():
        first, second, third, text = row['一级原因'], row['二级原因'], row['三级原因'], row['默认话术']

        # 查找一级原因
        first_child = next((item for item in result if item['label'] == first), None)
        if not first_child:
            counter['first'] += 1
            first_child = {"value": config_dict.get(first, str(counter['first'])), "label": first, "children": []}
            result.append(first_child)

        # 查找二级原因
        second_child = next((item for item in first_child['children'] if item['label'] == second), None)
        if not second_child:
            counter['second'] += 1
            second_child = {"value": config_dict.get(second, str(counter['second'])), "label": second, "children": []}
            first_child['children'].append(second_child)

        # 添加三级原因
        counter['third'] += 1
        third_child = {"value": config_dict.get(third, str(counter['third'])), "label": third, "text": text}
        second_child['children'].append(third_child)

    print(result)
