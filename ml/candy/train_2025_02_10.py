
"""
使用LSTM（长短期记忆网络）来训练CSV数据集。

feature:
1. 堆叠多个LSTM层可以增加模型的深度，使其能够学习到更复杂的特征和模式
2. 使用 hyperopt 优化模型超参数
hyperopt 可以通过定义超参数空间和目标函数，自动搜索最优的超参数组合

GridSearchCV 是一种穷举搜索方法，它会遍历所有指定的超参组合，找到最优的超参配置。虽然这种方法非常耗时，但可以确保找到最优解。
贝叶斯优化是一种更高效的超参优化方法，它通过构建目标函数的代理模型（如高斯过程）来预测超参的性能，并选择最有可能提升性能的超参组合

pip install hyperopt

@since 2025年1月2日 17:30:41
@see train_2025_01_02.py 参考模型
"""
from hyperopt import hp
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential


space = {
    'units': hp.choice('units', [30, 50, 70, 90, 120, 150, 200]),
    'dropout': hp.uniform('dropout', 0.1, 0.5),
    'optimizer': hp.choice('optimizer', ['adam', 'rmsprop']),
    'batch_size': hp.choice('batch_size', [8, 16, 32, 64]),
    'epochs': hp.choice('epochs', [20, 30, 50, 80])
}

# 读取CSV文件
# 假设你的CSV文件名为`data.csv`，前几列是特征，最后一列是目标值。
original_data = pd.read_csv('train.csv')

data = original_data.drop(['id', 'timestamp'], axis=1)

# 假设最后一列为target，其他列为特征
# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
features = data.iloc[:, :-1].values
target = data.iloc[:, -1].values

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
features_scaled = scaler.fit_transform(features)

# 将数据划分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, shuffle=False)

# 调整数据形状以适应LSTM输入 (samples, timesteps, features)
# 这里我们假设每个时间步长为1
X_train_tf = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test_tf = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# 定义 LSTM 模型
def create_model(params):
    model = Sequential()
    model.add(LSTM(params['units'], return_sequences=True, input_shape=(1, X_train_tf.shape[2]), dropout=params['dropout']))
    model.add(Dropout(rate=params['dropout']))
    model.add(LSTM(params['units'], dropout=params['dropout']))
    model.add(Dropout(rate=params['dropout']))
    model.add(Dense(1))
    model.compile(optimizer=params['optimizer'], loss='mean_squared_error')
    return model

# 定义目标函数
def objective(params):
    model = create_model(params)
    # model.fit(X_train_tf, y_train, epochs=30, batch_size=7, validation_data=(X_test_tf, y_test))
    model.fit(X_train_tf, y_train, epochs=params['epochs'], batch_size=params['batch_size'], verbose=0)
    loss = model.evaluate(X_test_tf, y_test, verbose=0)
    return {'loss': loss, 'status': STATUS_OK}


# 运行超参数优化
# 100%|██████████| 50/50 [09:08<00:00, 10.98s/trial, best loss: 0.8673014044761658]
trials = Trials()
best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=50, trials=trials)

# 输出最优超参数
print("Best Hyperparameters:", best)

# 将索引转换为实际值
best_params = {
    'units': [30, 50, 70, 90, 120, 150, 200][best['units']],
    'dropout': best['dropout'],
    'optimizer': ['adam', 'rmsprop'][best['optimizer']],
    'batch_size': [8, 16, 32, 64][best['batch_size']],
    'epochs': [20, 30, 50, 80][best['epochs']]
}
# Best Hyperparameters (actual values): {'units': 50, 'dropout': 0.11108671190174817, 'optimizer': 'adam', 'batch_size': 8, 'epochs': 80}
print("Best Hyperparameters (actual values):", best_params)