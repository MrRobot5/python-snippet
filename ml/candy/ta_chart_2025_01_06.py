
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
from matplotlib.widgets import Slider
from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.volume import VolumePriceTrendIndicator
from ta.momentum import RSIIndicator

# Load datas
data = pd.read_csv('predict.csv')
print(data.head())

# Clean NaN values
# df = ta.utils.dropna(df)

# Initialize Bollinger Bands Indicator
# https://github.com/bukosabino/ta
indicator_macd = MACD(close=data["close"])
indicator_vpt = VolumePriceTrendIndicator(close=data["close"], volume=data["volume"])
indicator_bb = BollingerBands(close=data["close"], window=20, window_dev=2)
indicator_rsi = RSIIndicator(close=data["close"])

# 创建一个图形对象和子图
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.1, bottom=0.25)  # 为滑动条预留空间

# 绘制折线图
# 绘制折线图，并使用行索引用作x轴。
ax.plot(data.index, data['close'])
ax.plot(data.index, indicator_bb.bollinger_mavg())
ax.plot(data.index, indicator_bb.bollinger_hband())
ax.plot(data.index, indicator_bb.bollinger_lband())

# ax.plot(data.index, indicator_macd.macd())
# ax.plot(data.index, indicator_macd.macd_diff())

# ax.plot(data.index, indicator_vpt.volume_price_trend())

# ax.plot(data.index, indicator_rsi.rsi())

# 设置x轴标签
ax.set_xticks(data.index)
ax.set_xticklabels(data.index, rotation=90)

# 标注调用量大于3000的节点
point = 5
for i, row in data.iterrows():
    # return_scaled, 分界线暂定 0.36。通过拨动分界点，调整S_n_B 的timing (待验证)
    if row['pred'] >= point:
        # f'{row["pred"]}: {row["pred"]}',
        ax.annotate('b' + str(row['pred']),
                    xy=(i, row['close']),
                    xytext=(i, row['close']),
                    arrowprops=dict(facecolor='black', shrink=0.05))
    if row['pred'] < point:
        # f'{row["pred"]}: {row["pred"]}',
        ax.annotate('s' + str(row['pred']),
                    xy=(i, row['close']),
                    xytext=(i, row['close']),
                    arrowprops=dict(facecolor='blue', shrink=0.05))

# 设置图形标题和标签
ax.set_title('Bollinger Bands')
ax.set_xlabel('index')
ax.set_ylabel('close')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend(loc='upper left')

# 创建滑动条
slider_ax = plt.axes([0.1, 0.1, 0.8, 0.03])  # [left, bottom, width, height]
slider = Slider(
    slider_ax,
    'Offset',
    0.0,
    len(data) - 100,  # 最大偏移量
    valinit=0,
    valstep=20
)

# 更新函数
def update(val):
    start = int(val)
    end = start + 100
    # 动态调整x轴范围
    ax.set_xlim(start, end)
    # 更新标题显示当前范围
    ax.set_title(f'Comparison ({start}-{end})', fontsize=14)
    # 重绘图形
    fig.canvas.draw_idle()

# 绑定事件
slider.on_changed(update)

# 强制初始化显示0-100范围
ax.set_xlim(0, 100)

# 显示图形
plt.show()
