
"""
使用 chatgpt 生成的代码。用于快速统计日志关键词频次
@since 2023-06-30 15:06:38
"""

if __name__ == '__main__':
    # 打开文件
    with open('C:/Users/yangpan3/Downloads/crm-foundation-all.log', 'r', encoding='UTF-8') as file:
        # 读取文件内容
        data = file.read()
        # 将所有单词转换为小写，并按空格分割成列表
        words = data.lower().split()
        # 创建一个空字典用于存储单词计数
        word_count = {}
        # 遍历单词列表，统计每个单词出现的次数
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        # 按照单词出现次数倒序排列字典
        sorted_word_count = dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))
        # 输出结果
        print(sorted_word_count)
