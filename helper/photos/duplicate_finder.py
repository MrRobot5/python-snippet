"""
重复文件清理

根据 output.txt 中的文件名删除 D:/Camera 下对应的文件，并打印操作结果。
find /e/所有照片 -type f -printf "%P\n" > output.txt
@since 2025年2月23日
"""

import os

# 定义目标文件夹路径
target_folder = "D:/Camera"

# 定义 output.txt 文件路径
txt_file_path = "output.txt"

# 确保目标文件夹存在
if not os.path.exists(target_folder):
    print(f"目标文件夹 {target_folder} 不存在。")
    exit()

# 打开 output.txt 文件并逐行读取
try:
    with open(txt_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"文件 {txt_file_path} 未找到。")
    exit()

# 遍历每一行，提取文件名并删除对应的文件
for line in lines:
    # 去除行首行尾的空白字符
    line = line.strip()
    # 提取文件名（忽略路径部分）
    filename = os.path.basename(line)
    # 构造目标文件的完整路径
    target_file_path = os.path.join(target_folder, filename)

    # 检查文件是否存在
    if os.path.exists(target_file_path):
        try:
            os.remove(target_file_path)
            print(f"已删除文件：{target_file_path}")
        except Exception as e:
            print(f"删除文件 {target_file_path} 时出错：{e}")
    else:
        print(f"文件 {target_file_path} 不存在，跳过。")