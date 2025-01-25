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

from sklearn.preprocessing import KBinsDiscretizer
import numpy as np

# 给定的一维数据
data = np.array([-0.1867, 0.3224, 0.4072, 0.2715, 0.3478, -0.1527, -0.3733, 0.1272, 0.8398, 1.264, 0.5684, 0.5175, -0.4072, -0.7126, -0.5429])

# 创建KBinsDiscretizer实例，选择3个区间，使用等宽离散化
kbins = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='uniform')

# 拟合并转换数据，注意需要将一维数据转换为二维形式
discretized_data = kbins.fit_transform(data.reshape(-1, 1))

# 将离散化后的结果转换回一维数组
discretized_data = discretized_data.flatten()

# 输出离散化后的结果
print("离散化后的结果：")
print(discretized_data)

# 计算每个离散值的占比
unique, counts = np.unique(discretized_data, return_counts=True)
total = len(data)
proportions = counts / total

# 输出占比
print("每个离散值的占比：")
for i, prop in enumerate(proportions):
    print(f"离散值 {i}: {prop:.2f}")