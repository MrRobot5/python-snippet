
"""
使用hyperopt 优化 LSTM模型超参数。

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
    'units': hp.choice('units', [30, 50, 90, 120, 150, 200]),
    'dropout': hp.uniform('dropout', 0.1, 0.5),
    'optimizer': hp.choice('optimizer', ['adam', 'rmsprop']),
    'batch_size': hp.choice('batch_size', [8, 16, 32, 64]),
    'epochs': hp.choice('epochs', [30, 50, 80, 100])
}

# 读取CSV文件
df_train = pd.read_csv('train.csv')

selected_columns = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']

# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
df_feature_train = df_train.loc[:, selected_columns].copy().values

timestep = 10  # use days to predict next 1 day return

scaler = MinMaxScaler(feature_range=(0, 1))
df_feature_train = scaler.fit_transform(df_feature_train)

# 调整数据形状以适应LSTM输入 (samples, timesteps, features)
x_train = []
y_train = []
for i in range(timestep, df_feature_train.shape[0]):  # discard the last "timestep" days
    x_train.append(df_feature_train[i - timestep:i])  # rolling_timestep * features
    y_train.append(df_train[['return']].iloc[i].values)  # days * (no rolling_timestep) * features
y_train = scaler.fit_transform(y_train)
x_train, y_train = np.array(x_train), np.array(y_train)

# 将数据划分为训练集和测试集
# (x_train, y_train)
# (x_test, y_test)
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, shuffle=False)

# 定义 LSTM 模型
def create_model(params):
    model = Sequential()
    model.add(LSTM(params['units'], return_sequences=True, input_shape=(timestep, x_train.shape[2]), dropout=params['dropout']))
    model.add(Dropout(rate=params['dropout']))
    model.add(LSTM(params['units'], dropout=params['dropout'],return_sequences=True))
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
    model.fit(x_train, y_train, epochs=params['epochs'], batch_size=params['batch_size'], verbose=0)
    loss = model.evaluate(x_test, y_test, verbose=0)
    return {'loss': loss, 'status': STATUS_OK}


# 运行超参数优化
# 100%|██████████| 50/50 [09:08<00:00, 10.98s/trial, best loss: 0.8673014044761658]
# 100%|██████████| 50/50 [28:25<00:00, 34.11s/trial, best loss: 0.020789314061403275] scale return
# 100%|██████████| 100/100 [48:25<00:00, 29.06s/trial, best loss: 0.014476322568953037] loss function
trials = Trials()
best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=100, trials=trials)

# 输出最优超参数
print("Best Hyperparameters:", best)

# 将索引转换为实际值
best_params = {
    'units': [30, 50, 90, 120, 150, 200][best['units']],
    'dropout': best['dropout'],
    'optimizer': ['adam', 'rmsprop'][best['optimizer']],
    'batch_size': [8, 16, 32, 64][best['batch_size']],
    'epochs': [30, 50, 80, 100][best['epochs']]
}
# Best Hyperparameters (actual values): {'units': 50, 'dropout': 0.11108671190174817, 'optimizer': 'adam', 'batch_size': 8, 'epochs': 80}
# Best Hyperparameters (actual values): {'units': 30, 'dropout': 0.20213520711415833, 'optimizer': 'rmsprop', 'loss': 'mean_squared_logarithmic_error', 'batch_size': 32, 'epochs': 30}
print("Best Hyperparameters (actual values):", best_params)