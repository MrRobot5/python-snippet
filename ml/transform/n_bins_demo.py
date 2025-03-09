"""
将连续数据划分为区间。
使用 KBinsDiscretizer 类来将一维数组根据区间划分为指定数量的类别。
KBinsDiscretizer 可以将连续特征离散化为等宽、等频或基于 k-means 的区间。

Binarizer
根据阈值对数据进行二值化（将要素值设置为0或1）
大于阈值的值映射为1，而小于或等于阈值的值映射为0。默认阈值为0时，仅正值映射为1。
二值化是对文本计数数据的常见操作，分析人员可以决定仅考虑某个功能的存在或不存在，而不考虑例如量化的出现次数。

@since 2025年1月8日 18:30:57
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 给定的一维数据
# data = np.array([-0.1867, 0.3224, 0.4072, 0.2715, 0.3478, -0.1527, -0.3733, 0.1272, 0.8398, 1.264, 0.5684, 0.5175, -0.4072, -0.7126, -0.5429])
# 1. 读取 CSV 文件
df = pd.read_csv('train.csv')  # 替换为你的文件路径

# 创建KBinsDiscretizer实例，选择3个区间，使用等宽离散化
# n_bins=10: 划分为 10 个类别。
# encode='ordinal': 输出为 0~9 的有序整数编码。
# strategy='quantile' 分箱基于数据分布的百分比位置，而非绝对数值范围，避免极值拉大分箱宽度。
# 等宽（uniform）策略，某些极端值会影响分箱的均匀性，使得大部分数据集中在某个区间，而其他区间样本很少。（计算每个离散值的占比可以观察到）❌
discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')

# 拟合并转换数据，注意需要将一维数据转换为二维形式
# discretized_data = discretizer.fit_transform(data.reshape(-1, 1))
df['fault_encoded'] = discretizer.fit_transform(df[['return']])
# discretized_data = discretizer.fit_transform(df[['return']])
# analyze_discretized_data(discretized_data)

# 查看结果
print(df.head())

df = df[:500]


def visualize_data_comparison(df):
    """
    可视化比较原始数据和离散化后的数据
    参数:
        df (DataFrame): 包含原始数据和离散化数据的数据框
    """
    # 数据准备
    original_values = df['return']
    discretized_values = df['fault_encoded'] * 0.1  # 保持量级一致

    # 创建画布和坐标系
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(left=0.1, bottom=0.25)  # 为滑动条预留空间

    # 绘制数据线
    # 设置统一线宽和透明度参数 (linewidth=1.5, alpha=0.7)
    line_original, = ax.plot(original_values, label='Original Data', marker='o', alpha=0.7, linewidth=1.5)
    line_discretized, = ax.plot(discretized_values, label='Discretized Data', marker='x', alpha=0.7, linewidth=1.5)

    # 设置图表样式
    ax.set_title('Comparison of Original and Discretized Values', fontsize=14)
    ax.set_xlabel('Index', fontsize=12)
    ax.set_ylabel('Value', fontsize=12)
    # 增加网格线 (ax.grid()) 提高可读性
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend(loc='upper left')

    # 创建滑动条
    slider_ax = plt.axes([0.1, 0.1, 0.8, 0.03])  # [left, bottom, width, height]
    slider = Slider(
        slider_ax,
        'Offset',
        0.0,
        len(original_values) - 100,  # 最大偏移量
        valinit=0,
        valstep=1
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


# 绘制图表
visualize_data_comparison(df)


def analyze_discretized_data(discretized_data):
    # 将离散化后的结果转换回一维数组
    discretized_data = discretized_data.flatten()

    # 输出离散化后的结果
    print("离散化后的结果：")
    print(discretized_data)

    # 计算每个离散值的占比
    unique, counts = np.unique(discretized_data, return_counts=True)
    total = df.shape[0]
    proportions = counts / total

    # 输出占比
    print("每个离散值的占比：")
    for i, prop in enumerate(proportions):
        print(f"离散值 {i}: {prop:.2f}")