"""
使用LSTM（长短期记忆网络）来训练CSV数据集。
特性：
0. target/y 连续特征离散化（回归改为分类）
1. 使用激活函数输出固定的类别/概率，帮助模型评估准确率（目标更明确，评估准确率更高）
2. 优化器、损失函数和评估指标适配修改

tensorboard==2.15.1

源数据： train.csv

@since 2025年1月2日 17:30:41
"""

import datetime
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint

# 为了保证代码的可重复性
np.random.seed(42)

# 读取CSV文件
# 假设你的CSV文件名为`data.csv`，前几列是特征，最后一列是目标值。
df_data = pd.read_csv('train.csv')

# 将数据划分为训练集和测试集
# Tips: 始终先将数据分成训练和测试子集，特别是在任何预处理步骤之前。https://scikit-learn.org/stable/common_pitfalls.html
# 防止 df_test 污染 scaler.fit(df_train)
df_train, df_test = train_test_split(df_data, test_size=0.2, shuffle=False)

selected_columns = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']

# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
df_feature_train = df_train.loc[:, selected_columns].copy().values
df_feature_test = df_test.loc[:, selected_columns].copy().values

# 定义时间步长为 20 天，表示使用过去 20 天的数据来预测下一天的返回值。
timestep = 10  # use days to predict next 1 day return

# 数据归一化
x_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler = MaxAbsScaler()
df_feature_train = x_scaler.fit_transform(df_feature_train)
df_feature_test = x_scaler.transform(df_feature_test)

# 调整数据形状以适应LSTM输入 (samples, timesteps, features)
x_train = []
y_train = []
for i in range(timestep, df_feature_train.shape[0]):  # discard the last "timestep" days
    x_train.append(df_feature_train[i - timestep:i])  # rolling_timestep * features
    y_train.append(df_train[['return']].iloc[i].values)  # days * (no rolling_timestep) * features
# 暂时使用 scaler 处理return, 负数结果train loss 难以评估
y_train = y_scaler.fit_transform(y_train)
x_train, y_train = np.array(x_train), np.array(y_train)

x_test = []
y_test = []
for i in range(timestep, df_feature_test.shape[0]):  # discard the last "timestep" days
    x_test.append(df_feature_test[i - timestep:i])  # rolling_timestep * features
    y_test.append(df_train[['return']].iloc[i].values)
y_test = y_scaler.transform(y_test)
x_test, y_test = np.array(x_test), np.array(y_test)


# 指定日志目录（每次训练需新建目录）
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

# 清晰地追踪LSTM模型的训练动态，优化超参数（如学习率、隐藏层数），并诊断训练中的问题（如过拟合、梯度异常）。
# tensorboard --logdir logs/fit/
tensorboard_callback = TensorBoard(
    log_dir=log_dir,          # 日志保存路径
    histogram_freq=1,       # 每隔1个epoch绘制权重直方图
    write_graph=True,        # 绘制计算图
    write_images=True       # 可视化激活函数（需安装graphviz）
)

# 保存最佳模型
# 确保训练时提供了足够的验证数据（通过 validation_split 或 validation_data）。
checkpoint_callback = ModelCheckpoint('best_model.keras', save_best_only=True)

# 定义LSTM模型
# Sequential模型是一个线性堆叠的层的容器，可以方便地按顺序添加层。
model = Sequential()
# Best Hyperparameters
hp = {'units': 120, 'dropout': 0.4257423014049223, 'optimizer': 'rmsprop', 'batch_size': 64, 'epochs': 50}
# units=50 number of memory cells, less could be underfitting
model.add(LSTM(hp['units'], return_sequences=True, input_shape=(timestep, x_train.shape[2]), dropout=hp['dropout']))
model.add(Dropout(rate=hp['dropout']))
model.add(LSTM(hp['units'], dropout=hp['dropout'], return_sequences=True))
model.add(Dropout(rate=hp['dropout']))
# 由于没有指定return_sequences=True，所以这个层只输出最后一个时间步的输出，这通常是用于预测任务的最后一步.
model.add(LSTM(hp['units'], dropout=hp['dropout']))
model.add(Dropout(rate=hp['dropout']))
model.add(Dense(1))

model.compile(optimizer=hp['optimizer'], loss='mean_squared_error')
# todo: 激活函数
# model.add(Dense(1, activation='softmax'))

# todo: 损失函数和评估指标
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 训练模型
# 初始化 TensorBoard 回调
model.fit(x_train, y_train, epochs=hp['epochs'], batch_size=hp['batch_size'], validation_data=(x_test, y_test), callbacks=[tensorboard_callback, checkpoint_callback])

# 保存模型
model.save('my_model.keras')
joblib.dump(x_scaler, 'x_scaler.pkl')
joblib.dump(y_scaler, 'y_scaler.pkl')

# 进行预测
y_pred = model.predict(x_test)

# 反归一化数据
# original_test = scaler.inverse_transform(X_test)

# 计算均方误差 (MSE)
mse = mean_squared_error(y_test, y_pred)
# MSE of prediction for test set is: 2.1925%
print(f'MSE of prediction for test set is: {round(mse * 100, 4)}%')

# test_loss, test_acc = model.evaluate(X_test_tf, y_test)
# print(f"Test accuracy: {test_acc:.4f}")