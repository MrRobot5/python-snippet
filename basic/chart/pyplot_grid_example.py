import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
zh_font = fm.FontProperties(fname='C:/Windows/Fonts/simhei.ttf')

# 示例数据
categories = ['类别A', '类别B', '类别C', '类别D', '类别E']
bar_values = [5, 7, 3, 8, 4]
line1_values = [2, 6, 4, 7, 5]
line2_values = [3, 5, 2, 6, 4]

# 创建一个新的图表
fig = plt.figure(figsize=(10, 6))

# 使用 subplot2grid 创建子图
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)  # 占据第一行的两个单元格
ax2 = plt.subplot2grid((2, 2), (1, 0))  # 占据第二行的第一个单元格
ax3 = plt.subplot2grid((2, 2), (1, 1))  # 占据第二行的第二个单元格

# 在第一个子图中画柱状图
ax1.bar(categories, bar_values, color='b', alpha=0.6, label='柱状图')
ax1.set_xlabel('类别', fontproperties=zh_font)
ax1.set_ylabel('柱状图值', fontproperties=zh_font)
ax1.set_title('柱状图', fontproperties=zh_font)
ax1.legend(prop=zh_font)

# 在第二个子图中画第一个折线图
ax2.plot(categories, line1_values, color='r', marker='o', linestyle='-', label='折线图1')
ax2.set_xlabel('类别', fontproperties=zh_font)
ax2.set_ylabel('折线图值1', fontproperties=zh_font)
ax2.set_title('折线图1', fontproperties=zh_font)
ax2.legend(prop=zh_font)

# 在第三个子图中画第二个折线图
ax3.plot(categories, line2_values, color='g', marker='s', linestyle='--', label='折线图2')
ax3.set_xlabel('类别', fontproperties=zh_font)
ax3.set_ylabel('折线图值2', fontproperties=zh_font)
ax3.set_title('折线图2', fontproperties=zh_font)
ax3.legend(prop=zh_font)

# 调整子图之间的间距
plt.tight_layout()

# 显示图表
plt.show()