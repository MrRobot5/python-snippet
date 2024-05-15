import re

"""
功能： 使用正则提取字符串
prompt: 提取代码片段中，value 值，输出为数组
@since 2024年5月15日 14:15:00 chat-gpt
"""

html_content = '''
   <option value="201" dataKey="()" >Apple</option>
   <option value="202" dataKey="()" >Banana</option>
   <option value="203" dataKey="()" >Cherry</option>
   <option value="204" dataKey="()" >Durian</option>
'''

# 使用正则表达式匹配所有的value属性
# (\d+): 这是一个捕获组，用圆括号()表示。\d匹配任何数字（等价于[0-9]），+表示匹配前面的字符一次或多次。所以，\d+匹配一个或多个数字。整个捕获组的意思是匹配并捕获一个或多个数字。
values = re.findall(r'value="(\d+)"', html_content)

# 输出结果 ['201', '202', '203', '204']
print(values)
