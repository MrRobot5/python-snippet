
"""
使用LSTM（长短期记忆网络）来训练CSV数据集。
步骤包括数据预处理、模型定义、训练和评估。
源数据： train.csv

@since 2025年1月2日 17:30:41
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

# 为了保证代码的可重复性
np.random.seed(42)

# 读取CSV文件
# 假设你的CSV文件名为`data.csv`，前几列是特征，最后一列是目标值。
original_data = pd.read_csv('train.csv')

data = original_data.drop(['id', 'timestamp'], axis=1)

# 假设最后一列为target，其他列为特征
# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
features = data.iloc[:, :-1].values
target = data.iloc[:, -1].values

# 数据归一化
"""
`MinMaxScaler` 是 scikit-learn 库中用于特征缩放的一个类。
它通过将特征值缩放到一个范围（通常是 [0, 1]）来标准化数据。具体来说，它将每个特征的值线性变换到指定的最小值和最大值之间。
使用 `MinMaxScaler` 可以有效地将不同范围的特征值缩放到相同的范围，使得机器学习模型更容易处理和训练。
"""
scaler = MinMaxScaler(feature_range=(0, 10))
features_scaled = scaler.fit_transform(features)

# 将数据划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, shuffle=False)

# 调整数据形状以适应LSTM输入 (samples, timesteps, features)
# 这里我们假设每个时间步长为1
X_train_tf = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test_tf = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# 定义LSTM模型
# Sequential模型是一个线性堆叠的层的容器，可以方便地按顺序添加层。
model = Sequential()
# return_sequences=True：这个参数表示该层的输出应该包含整个序列的输出，而不是只输出最后一个时间步的输出。这对于后续的LSTM层来说是必要的，因为后续的LSTM层需要接收整个序列的信息.
# input_shape=(1, X_train_tf.shape[2])：定义了输入数据的形状。1表示时间序列的长度（即时间步数），X_train_tf.shape[2]表示每个时间步的特征数量。
# dropout=0.2：这个参数表示在训练过程中，每个时间步的输入将有20%的概率被丢弃。这意味着在每个时间步，输入特征的一部分将被随机设置为零，从而减少模型对特定输入特征的依赖.
model.add(LSTM(50, return_sequences=True, input_shape=(1, X_train_tf.shape[2]), dropout=0.2))
model.add(Dropout(rate=0.2))
# 由于没有指定return_sequences=True，所以这个层只输出最后一个时间步的输出，这通常是用于预测任务的最后一步.
model.add(LSTM(50, dropout=0.2))
model.add(Dropout(rate=0.2))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# 训练模型
model.fit(X_train_tf, y_train, epochs=30, batch_size=7, validation_data=(X_test_tf, y_test))

# 保存模型
model.save('my_model.h5')  # HDF5文件格式

# 进行预测
y_pred = model.predict(X_test_tf)

# 反归一化数据
# original_test = scaler.inverse_transform(X_test)

# 导出数据和预测结果到 csv
# 将数组转换回DataFrame: 使用pd.DataFrame()构造函数将数组转换回DataFrame
# original_test = pd.DataFrame(X_test, columns=data.columns[:-1])
# original_test["pred"] = y_pred
# original_test.to_csv('output_pred.csv', index=False)

# 计算均方误差 (MSE)
# 它计算的是模型预测值与实际值之间的均方误差（Mean Squared Error，简称 MSE），是回归问题中常用的损失函数之一。
mse = mean_squared_error(y_test, y_pred)
# Mean Squared Error: 0.8883725388249385
print(f'Mean Squared Error: {mse}')
