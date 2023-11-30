# encoding=utf-8
import jieba

# Full Mode: 对/ 自身/ 发展/ 有/ 清晰/ 的/ 认知
seg_list = jieba.cut("对自身发展有清晰的认知", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

# Default Mode: 我/ 来到/ 北京/ 清华大学
seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))

