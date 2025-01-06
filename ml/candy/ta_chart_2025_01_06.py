
"""
绘制结果
源数据： predict.csv

pip install ta
Successfully installed ta-0.11.0

@since 2025年1月6日 17:29:02
"""

import ta
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import MACD

# Load datas
data = pd.read_csv('predict.csv')
print(data.head())

# Clean NaN values
# df = ta.utils.dropna(df)

# Initialize Bollinger Bands Indicator
# https://github.com/bukosabino/ta
indicator_macd = MACD(close=data["close"])

# Add MACD features
data['macd'] = indicator_macd.macd()
data['macd_diff'] = indicator_macd.macd_diff()

# 创建一个图形对象和子图
fig, ax = plt.subplots()

# 绘制折线图
# 绘制折线图，并使用行索引用作x轴。
ax.plot(data.index, data['close'], marker='o')
ax.plot(data.index, data['macd'], marker='^')
ax.plot(data.index, data['macd_diff'], marker='x')

# 设置x轴标签
ax.set_xticks(data.index)
ax.set_xticklabels(data.index, rotation=90)

# 标注调用量大于3000的节点
for i, row in data.iterrows():
    if row['pred'] > 0.2:
        # f'{row["pred"]}: {row["pred"]}',
        ax.annotate('b',
                    xy=(i, row['close']),
                    xytext=(i, row['close']),
                    arrowprops=dict(facecolor='black', shrink=0.05))

# 设置图形标题和标签
ax.set_title('Bollinger Bands')
ax.set_xlabel('index')
ax.set_ylabel('close')

# 显示图形
plt.show()
