"""
为每一行的文本添加序号。

prompt:
为以下文本的每一行增加序号。
文本为： 文本1
文本2

@since 2024年1月3日 14:11:01
"""

# 原始文本
text = """文本1
文本2"""

def numbered_format(text):
    # 按行分割文本
    lines = text.split('\n')

    # 为每一行添加序号
    numbered_lines = [f"{index + 1}. {line}" for index, line in enumerate(lines)]

    # 将处理后的文本合并回一个字符串
    numbered_text = '\n'.join(numbered_lines)

    print(numbered_text)

if __name__ == '__main__':
    for line in text.split("\n\n"):
        numbered_format(line)
