
"""
修改 jsf 配置，全部改为延时启动
prompt: 读取工程文件夹并遍历，获取所有的xml 文件，如果有<jsf:consumer 标签的元素，如果没有 lazy="true" 属性，就修改当前元素并加入 lazy="true" 属性。保存修改的文件，并且需要保留原文件中的注释。

pip install lxml

gpt 生产的脚本会存在bug 的情况。case: os.walk 返回值命名为 root, 同时，tree.getroot() 也命名为root， 导致运行时报错。🙉
@since 2024年2月4日 17:43:53
"""

import os
from lxml import etree

# 设置命名空间，如果你的 XML 使用了命名空间
namespaces = {'jsf': 'http://jsf.foo.com/schema/jsf', 'beans': 'http://www.springframework.org/schema/beans'}
# 使用 xml.etree.ElementTree 模块来处理 XML 文件
# 注册命名空间
# for prefix, uri in namespaces.items():
#     ET.register_namespace(prefix, uri)

# 遍历指定目录下的所有 XML 文件
for root, dirs, files in os.walk('/workspace/crm-project-management'):
    for file in files:
        # 如果当前目录中有 .idea 文件夹，则从遍历列表中移除
        if '.idea' in dirs:
            dirs.remove('.idea')

        if file.endswith('.xml'):
            file_path = os.path.join(root, file)
            parser = etree.XMLParser(remove_blank_text=False)
            tree = etree.parse(file_path, parser)
            root_element = tree.getroot()

            # 设置一个标志来跟踪是否进行了修改
            modified = False
            # 查找所有的 <jsf:consumer> 标签
            # './/jsf:consumer': 这是一个 XPath 表达式，用于指定要查找的元素。
            # . 表示当前元素（在这种情况下是根元素），// 是一个选择器，表示查找任何深度的子孙元素，jsf:consumer 是要查找的具体元素的标签名。
            for consumer in root_element.findall('.//jsf:consumer', namespaces):
                # 检查是否已经有 lazy="true" 属性
                if consumer.get('lazy') != 'true':
                    consumer.set('lazy', 'true')  # 设置 lazy="true" 属性
                    modified = True  # 标记已进行修改

            # 如果进行了修改，则保存文件
            if modified:
                # 使用 tree.write 方法保存文件时，pretty_print=True 参数确保了格式化输出，同时保留了注释。
                tree.write(file_path, encoding='utf-8', xml_declaration=True, pretty_print=True)
                print("modified: " + file_path)
