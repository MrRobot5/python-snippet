"""
使用LSTM（长短期记忆网络）来训练回归模型。
步骤包括数据预处理、模型定义、训练和评估。
源数据： train.csv

@todo:
1. 初始化两个独立的 scaler 对象， scaler_x  scaler_y
2. 保存 Scaler 参数：标准化后，需保存 scaler_x 和 scaler_y，以便后续对测试集 x_test 和 y_test 使用相同参数进行标准化。
3. 参考qlib 记录优化的实验结果

@since 2025年1月2日 17:30:41
"""
from utils import prepare_dataset
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

# 为了保证代码的可重复性
np.random.seed(42)

# 读取CSV文件
# 假设你的CSV文件名为`data.csv`，前几列是特征，最后一列是目标值。
df_data = pd.read_csv('train.csv')

# 将数据划分为训练集和测试集
# Tips: 始终先将数据分成训练和测试子集，特别是在任何预处理步骤之前。https://scikit-learn.org/stable/common_pitfalls.html
# 防止 df_test 污染 scaler.fit(df_train)
df_train, df_test = train_test_split(df_data, test_size=0.2, shuffle=False)

# use days to predict next 1 day return
TIMESTEPS = 10
SELECTED_FEATURES = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']
TARGET_COLUMN = 'return'

# 数据归一化
"""
`MinMaxScaler` 是 scikit-learn 库中用于特征缩放的一个类。
它通过将特征值缩放到一个范围（通常是 [0, 1]）来标准化数据。具体来说，它将每个特征的值线性变换到指定的最小值和最大值之间。
使用 `MinMaxScaler` 可以有效地将不同范围的特征值缩放到相同的范围，使得机器学习模型更容易处理和训练。
"""
x_scaler = MinMaxScaler(feature_range=(0, 1))
y_scaler = MinMaxScaler(feature_range=(0, 1))

# 处理训练集
x_train, y_train = prepare_dataset(
    df=df_train,
    selected_features=SELECTED_FEATURES,
    target_column=TARGET_COLUMN,
    timesteps=TIMESTEPS,
    x_scaler=x_scaler,
    y_scaler=y_scaler,
    fit=True
)

# 处理测试集
x_test, y_test = prepare_dataset(
    df=df_test,
    selected_features=SELECTED_FEATURES,
    target_column=TARGET_COLUMN,
    timesteps=TIMESTEPS,
    x_scaler=x_scaler,
    y_scaler=y_scaler,
    fit=False
)

# 定义LSTM模型
# Sequential模型是一个线性堆叠的层的容器，可以方便地按顺序添加层。
model = Sequential()
# Best Hyperparameters
hp = {'units': 120, 'dropout': 0.4257423014049223, 'optimizer': 'rmsprop', 'batch_size': 64, 'epochs': 50}
# units=50 number of memory cells, less could be underfitting
# return_sequences=True：这个参数表示该层的输出应该包含整个序列的输出，而不是只输出最后一个时间步的输出。这对于后续的LSTM层来说是必要的，因为后续的LSTM层需要接收整个序列的信息.
# input_shape=(timestep, X_train_tf.shape[2])：定义了输入数据的形状。timestep 表示时间序列的长度（即时间步数），X_train_tf.shape[2]表示每个时间步的特征数量。
# dropout=0.2：这个参数表示在训练过程中，每个时间步的输入将有20%的概率被丢弃。这意味着在每个时间步，输入特征的一部分将被随机设置为零，从而减少模型对特定输入特征的依赖.
model.add(LSTM(hp['units'], return_sequences=True, input_shape=(TIMESTEPS, x_train.shape[2]), dropout=hp['dropout']))
model.add(Dropout(rate=hp['dropout']))
model.add(LSTM(hp['units'], dropout=hp['dropout'], return_sequences=True))
model.add(Dropout(rate=hp['dropout']))
# 由于没有指定return_sequences=True，所以这个层只输出最后一个时间步的输出，这通常是用于预测任务的最后一步.
model.add(LSTM(hp['units'], dropout=hp['dropout']))
model.add(Dropout(rate=hp['dropout']))
model.add(Dense(1))

model.compile(optimizer=hp['optimizer'], loss='mean_squared_error')

# 训练模型
model.fit(x_train, y_train, epochs=hp['epochs'], batch_size=hp['batch_size'])

# 保存模型
model.save('my_model.keras')  # HDF5文件格式
joblib.dump(x_scaler, 'x_scaler.pkl')
joblib.dump(y_scaler, 'y_scaler.pkl')

# 进行预测
y_pred = model.predict(x_test)

# 反归一化数据
# original_test = scaler.inverse_transform(X_test)

# 计算均方误差 (MSE)
# 它计算的是模型预测值与实际值之间的均方误差（Mean Squared Error，简称 MSE），是回归问题中常用的损失函数之一。
mse = mean_squared_error(y_test, y_pred)

# 测试预测的结果导出，方便单独分析
result_df = pd.DataFrame(y_test, columns=["y_test"])
result_df["y_pred"] = y_pred
result_df.to_csv('test_predict.csv', index=False)

# Mean Squared Error: 0.8883725388249385
# MSE of prediction for test set is: 2.1925%
print(f'MSE of prediction for test set is: {round(mse * 100, 4)}%')
