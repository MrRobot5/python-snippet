"""
柱状图和两个折线图示例

@since 2025年1月6日 14:29:06

"""

import matplotlib.pyplot as plt

# 示例数据
categories = ['A', 'B', 'C', 'D', 'E']
bar_values = [5, 7, 3, 8, 4]
line1_values = [2, 6, 4, 7, 5]
line2_values = [3, 5, 2, 6, 4]

# 创建一个新的图表
fig, ax1 = plt.subplots()

# 画柱状图
ax1.bar(categories, bar_values, color='b', alpha=0.6, label='bar')

# 创建共享x轴的第二个y轴
ax2 = ax1.twinx()

# 画第一个折线图
ax2.plot(categories, line1_values, color='r', marker='o', linestyle='-', label='line-1')

# 画第二个折线图
ax2.plot(categories, line2_values, color='g', marker='s', linestyle='--', label='line-2')

# 添加标签和标题
ax1.set_xlabel('categories')
ax1.set_ylabel('bar_values')
ax2.set_ylabel('line_values')
plt.title('mix_chart_example')

# 添加图例
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))

# 显示图表
plt.show()