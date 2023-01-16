# -*- coding:utf-8 -*-

"""
    功能： 根据模板文件，生成类似的文件。
    案例： 批量改写弹窗，生成类似 el-dialog 文件
"""

# 导入 re 模块
import re


# 创建一个函数来替换文本
def replace_text(pattern, replace):
    # 以读写模式打开文件
    with open('SampleFile.txt', 'r+') as f:
        # 读取文件数据并将其存储在文件变量中
        file = f.read()

        # 用文件数据中的字符串替换模式
        file = re.sub(pattern, replace, file)

        # 设置位置到页面顶部插入数据
        f.seek(0)

        # 在文件中写入替换数据
        f.write(file)

        # 截断文件大小
        f.truncate()

    # 返回“文本已替换”字符串
    print("文本已替换")


def name_convert_to_camel(name: str) -> str:
    """下划线转驼峰(小驼峰)"""
    return re.sub(r'(_[a-z])', lambda x: x.group(1)[1].upper(), name)


def name_convert_to_snake(name: str) -> str:
    """驼峰转下划线"""
    if '_' not in name:
        name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    else:
        raise ValueError(f'{name}字符中包含下划线，无法转换')
    return name.lower()


def name_convert(name: str) -> str:
    """驼峰式命名和下划线式命名互转"""
    is_camel_name = True  # 是否为驼峰式命名
    if '_' in name and re.match(r'[a-zA-Z_]+$', name):
        is_camel_name = False
    elif re.match(r'[a-zA-Z]+$', name) is None:
        raise ValueError(f'Value of "name" is invalid: {name}')
    return name_convert_to_snake(name) if is_camel_name else name_convert_to_camel(name)


def decapitalize(string):
    return string[:1].lower() + string[1:]


if __name__ == '__main__':
    # 创建一个变量并存储我们要搜索的文本
    search_text = "World"
    # 创建一个变量并存储我们要更新的文本
    replace = "Universe"
    # 调用replace_text函数并打印返回的语句
    # replace_text(search_text, replace)
    # -> hello_world_world
    # 1, 2, 7, 12, 40, 16, 17, 18, 20
    name = "AssignmentDetailDialog"
    convert = name_convert(name)
    print(convert)
    print("<{} ref=\"{}\"></{}>".format(convert, decapitalize(name), convert))




