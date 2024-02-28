
"""
输出当前路径下的js后缀文件，格式为字符串："app_1.js", "app_3.js"

glob是Python中的一个模块，它提供了一个函数glob.glob()，该函数使用Unix shell风格的匹配模式来查找与指定模式匹配的文件路径。
模块名称glob来源于“global”或“globbing”，这是一种在Unix shell中用于文件名扩展的术语。

shell版本  echo $(ls *.js | sed 's/\(.*\)/"\1"/' | tr '\n' ', ' | sed 's/, $/\n/')
python压缩版本 print(', '.join(f'"{f}"' for f in __import__('glob').glob('*.js')))

"""

import glob

# 获取当前目录下所有的.js文件
js_files = glob.glob('*.js')

# 格式化文件名为带双引号的字符串
formatted_files = ', '.join(f'"{file}"' for file in js_files)

# 输出： "app_1.js", "app_3.js"
print(formatted_files)
