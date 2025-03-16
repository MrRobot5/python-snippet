
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
from utils import prepare_dataset
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential

space = {
    'num_layers': hp.choice('num_layers', [1, 2, 3, 4, 5]),  # 层数选择
    'units': hp.quniform('units', 16, 512, 16),     # 神经元数量，整数均匀分布（步长为16）
    'dropout': hp.uniform('dropout', 0.1, 0.5),
    'optimizer': hp.choice('optimizer', ['adam', 'rmsprop']),
    'batch_size': hp.choice('batch_size', [8, 16, 32, 64]),
    'epochs': hp.choice('epochs', [30, 50, 80, 100])
}

# 读取CSV文件
df_data = pd.read_csv('train.csv')

# use days to predict next 1 day return
TIMESTEPS = 10
SELECTED_FEATURES = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']
TARGET_COLUMN = 'return'

# 数据分割
df_train, df_test = train_test_split(df_data, test_size=0.2, shuffle=False)

# 初始化Scaler
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

# 定义 LSTM 模型
def create_model(params):
    model = Sequential()
    model.add(LSTM(int(params['units']), input_shape=(TIMESTEPS, x_train.shape[2]), dropout=params['dropout'], return_sequences=True))
    model.add(Dropout(rate=params['dropout']))
    # 添加LSTM层
    for i in range(params['num_layers']):
        model.add(LSTM(int(params['units']), dropout=params['dropout'], return_sequences=True))
        model.add(Dropout(rate=params['dropout']))

    model.add(LSTM(int(params['units']), dropout=params['dropout']))
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
best = fmin(fn=objective, space=space, algo=tpe.suggest, max_evals=50, trials=trials)

# 输出最优超参数
print("Best Hyperparameters:", best)

# 将索引转换为实际值
# Best Hyperparameters (actual values): {'units': 50, 'dropout': 0.11108671190174817, 'optimizer': 'adam', 'batch_size': 8, 'epochs': 80}
# Best Hyperparameters (actual values): {'units': 30, 'dropout': 0.20213520711415833, 'optimizer': 'rmsprop', 'loss': 'mean_squared_logarithmic_error', 'batch_size': 32, 'epochs': 30}
# print("Best Hyperparameters (actual values):", best_params)