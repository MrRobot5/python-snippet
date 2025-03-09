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
# desc_result(discretized_data)

# 查看结果
print(df.head())

df = df[:100]

# todo chart

# 提取 original 和 scaled 列
y_test = df['return'] # 假设列名为 'original'
y_pred = df['fault_encoded'] * 0.1  # 假设列名为 'scaled'

# 绘制折线图
plt.plot(y_test, label='y_test', marker='o')  # 添加标记以便更清晰[^2^]
plt.plot(y_pred, label='y_pred', marker='x')     # 添加标记以便更清晰[^2^]

# 添加标题和标签
plt.title('Original vs Scaled Values')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()  # 添加图例[^3^]

# 显示图表
plt.show()


def desc_result(discretized_data):
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