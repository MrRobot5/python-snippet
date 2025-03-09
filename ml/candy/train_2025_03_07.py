"""
使用hyperopt 优化 LSTM模型超参数。

pip install hyperopt

@since 2025年3月7日 13:22:00
@see train_2025_01_08.py 参考模型
"""
from hyperopt import hp
from hyperopt import fmin, tpe, hp, Trials, STATUS_OK
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, KBinsDiscretizer
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

# 定义超参数搜索空间
# quniform 是 Hyperopt 提供的一种参数分布类型，用于在连续区间内生成离散化均匀分布的候选值。它通过将连续区间分成 q 个等距的桶（quantization steps），从中随机选择一个值。
space = {
    'num_layers': hp.choice('num_layers', [1, 2, 3, 4, 5]),  # 层数选择
    'dropout': hp.uniform('dropout', 0.1, 0.5),
    'units': hp.quniform('units', 16, 256, 16),     # 神经元数量，整数均匀分布（步长为16）
    'activation': hp.choice('activation', ['tanh', 'relu']),  # 激活函数
    'learning_rate': hp.loguniform('learning_rate', -5, -2),  # 学习率范围, 对数均匀分布（用于学习率等浮点参数）
    'epochs': hp.choice('epochs', [20, 30, 40, 50, 60]),        # 训练轮数
    'batch_size': hp.quniform('batch_size', 32, 128, 32)  # 批量大小
}

# 读取CSV文件
df_train = pd.read_csv('train.csv')

selected_columns = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']

# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
df_feature_train = df_train.loc[:, selected_columns].copy().values

timestep = 10  # use days to predict next 1 day return

scaler = MinMaxScaler(feature_range=(0, 1))
# 连续数据转为分类
discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
df_feature_train = scaler.fit_transform(df_feature_train)

# 调整数据形状以适应LSTM输入 (samples, timesteps, features)
x_train = []
y_train = []
for i in range(timestep, df_feature_train.shape[0]):  # discard the last "timestep" days
    x_train.append(df_feature_train[i - timestep:i])  # rolling_timestep * features
    y_train.append(df_train[['return']].iloc[i].values)  # days * (no rolling_timestep) * features
y_train = discretizer.fit_transform(y_train)
x_train, y_train = np.array(x_train), np.array(y_train)

# 将数据划分为训练集和测试集
# (x_train, y_train)
# (x_test, y_test)
# x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, shuffle=False)

# 转换为独热编码标签
y_train = to_categorical(y_train, 10)


# 定义 LSTM 模型
def create_model(hp):
    """根据超参数构建Keras模型"""
    model = Sequential()
    model.add(LSTM(int(hp['units']), input_shape=(timestep, x_train.shape[2]), dropout=hp['dropout'], return_sequences=True))

    # 添加LSTM层
    for i in range(hp['num_layers']):
        model.add(LSTM(units=int(hp['units']), activation=hp['activation'], dropout=hp['dropout'], return_sequences=True))
        model.add(Dropout(rate=hp['dropout']))

    model.add(LSTM(units=int(hp['units']), activation=hp['activation']))
    model.add(Dropout(rate=hp['dropout']))
    model.add(Dense(10, activation='softmax'))

    # 编译模型
    optimizer = Adam(learning_rate=hp['learning_rate'])
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# 定义目标函数
def objective(hp):
    """目标函数：返回验证准确率"""
    model = create_model(hp)
    early_stop = EarlyStopping(monitor='val_loss', patience=5)
    history = model.fit(
        x_train, y_train,
        epochs=hp['epochs'],
        batch_size=int(hp['batch_size']),
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=0  # 减少训练输出
    )
    print(f"Val accuracy history: {history.history['val_accuracy']}")

    # 平均验证准确率
    # average_val_accuracy = np.mean(history.history['val_accuracy'])
    # return -average_val_accuracy
    # 最佳验证准确率（峰值）
    # max_val_accuracy = max(history.history['val_accuracy'])
    # return -max_val_accuracy
    # 早停法最佳验证准确率
    return -history.history['val_accuracy'][-1]


# 执行优化搜索
trials = Trials()
best = fmin(
    objective,
    space,
    algo=tpe.suggest,  # 使用TPE算法
    max_evals=50,      # 最大尝试次数
    trials=trials
)

# 输出最优超参数
print(f'\n最优超参数：{best}')
print(f'最佳验证准确率：{-best["result"]:.4f}')