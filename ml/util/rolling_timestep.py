
"""
构造 LSTM模型 时间序列数据
从一个包含特征和目标变量的训练数据集中提取时间序列特征和目标值

@since 2025年2月20日 15:05:26
"""


import pandas as pd
import numpy as np

# 创建一个模拟的训练数据集
data = {
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
    'return': np.random.rand(100)
}
df_train = pd.DataFrame(data)

# 运行原始代码
# .loc[:, df_train.columns.str.contains('feature')] 选择所有列名中包含字符串 'feature' 的列，提取这些列作为特征数据。
# .copy()：确保提取的数据是独立的副本，避免对原始数据的修改。
# df_feature_train = df_train.loc[:, df_train.columns.str.contains('feature')].copy().values
selected_columns = ["feature1", "feature2"]
df_feature_train = df_train.loc[:, selected_columns].copy().values
# 定义时间步长为 60 天，表示使用过去 60 天的数据来预测下一天的返回值。
timestep = 60  # use days to predict next 1 day return
x_train = []
y_train = []
for i in range(timestep, df_feature_train.shape[0]):  # discard the last "timestep" days
    # 提取从 i - timestep 到 i 的特征数据（即过去 60 天的特征），并将其添加到 x_train 列表中。
    x_train.append(df_feature_train[i - timestep:i])  # rolling_timestep * features
    # 提取第 i 行的目标值（return 列），并将其添加到 y_train 列表中。
    y_train.append(df_train[['return']].iloc[i].values)  # days * (no rolling_timestep) * features
x_train, y_train = np.array(x_train), np.array(y_train)

# 输出结果
print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)
print("x_train sample:", x_train[0])
print("y_train sample:", y_train[0])