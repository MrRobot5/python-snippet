import random
import string

"""
生成指定的 txt 文件
@since 2024年2月28日 16:32:16 chat-gpt
"""

# 指定文件名
filename = "output.txt"

# 定义一个函数来生成随机字符串
def get_random_string(length=10):
    # 定义随机字符串的可能字符
    letters = string.ascii_letters + string.digits
    # 生成随机字符串
    return ''.join(random.choice(letters) for i in range(length))

# 打开文件准备写入
with open(filename, "w") as file:
    # 循环200次
    for i in range(200):
        # 每100行写入一次字符串"@合同编号@"
        for j in range(99):  # 写入199行随机字符串
            file.write(get_random_string() + "\n")
        file.write("@合同编号@\n")  # 第200行写入特定字符串

# 文件写入完成后会自动关闭
