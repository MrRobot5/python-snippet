"""
使用LSTM（长短期记忆网络）来训练分类模型。
特性：
0. target/y 连续特征离散化（回归改为分类）
1. 使用激活函数输出固定的类别/概率，帮助模型评估准确率（目标更明确，评估准确率更高）
2. 优化器、损失函数和评估指标适配修改

tensorboard==2.15.1

源数据： train.csv

@see train_2025_01_02.py 区别：损失函数、激活函数、输出层结构、标签编码方式以及评估指标。
@since 2025年1月2日 17:30:41
"""

from utils import prepare_dataset
import datetime
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, KBinsDiscretizer
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping
from tensorflow.keras.utils import to_categorical

# todo 尝试双向LSTM (LSTM(..., bidirectional=True))
# todo 在模型中添加注意力机制提升分类效果

# 为了保证代码的可重复性
np.random.seed(42)

# 读取CSV文件
# 假设你的CSV文件名为`data.csv`，前几列是特征，最后一列是目标值。
df_data = pd.read_csv('train.csv')

# 分成10个类别
# 输出层神经元数量必须等于分类类别数（这里是10）
num_classes=10

# 将数据划分为训练集和测试集
# Tips: 始终先将数据分成训练和测试子集，特别是在任何预处理步骤之前。https://scikit-learn.org/stable/common_pitfalls.html
# 防止 df_test 污染 scaler.fit(df_train)
df_train, df_test = train_test_split(df_data, test_size=0.2, shuffle=False)

# 定义时间步长为 20 天，表示使用过去 20 天的数据来预测下一天的返回值。
TIMESTEPS = 10  # use days to predict next 1 day return
SELECTED_FEATURES = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']
TARGET_COLUMN = 'return'

# 数据归一化
x_scaler = MinMaxScaler(feature_range=(0, 1))
# 连续数据转为分类
discretizer = KBinsDiscretizer(n_bins=num_classes, encode='ordinal', strategy='quantile')

# 处理训练集
x_train, y_train = prepare_dataset(
    df=df_train,
    selected_features=SELECTED_FEATURES,
    target_column=TARGET_COLUMN,
    timesteps=TIMESTEPS,
    x_scaler=x_scaler,
    y_scaler=discretizer,
    fit=True
)

# 处理测试集
x_test, y_test = prepare_dataset(
    df=df_test,
    selected_features=SELECTED_FEATURES,
    target_column=TARGET_COLUMN,
    timesteps=TIMESTEPS,
    x_scaler=x_scaler,
    y_scaler=discretizer,
    fit=False
)

# 转换为独热编码标签
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

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
checkpoint_callback = ModelCheckpoint('best_model.keras', monitor='val_accuracy', mode='max', save_best_only=True, verbose=1)

# 使用EarlyStopping防止过拟合
early_stop = EarlyStopping(monitor='val_loss', patience=5)

# 定义LSTM模型
# Sequential模型是一个线性堆叠的层的容器，可以方便地按顺序添加层。
model = Sequential()
# Best Hyperparameters
hp = {'units': 224, 'dropout': 0.1615750616970508, 'activation': 'tanh', 'batch_size': 32, 'epochs': 30, 'learning_rate': 0.007036898684888372}
# units=50 number of memory cells, less could be underfitting

model.add(LSTM(hp['units'], input_shape=(TIMESTEPS, x_train.shape[2]), dropout=hp['dropout'], activation=hp['activation'], bidirectional=True, return_sequences=True))
model.add(Dropout(rate=hp['dropout']))
model.add(LSTM(hp['units'], dropout=hp['dropout'], activation=hp['activation'], return_sequences=True))
model.add(Dropout(rate=hp['dropout']))
model.add(LSTM(hp['units'], activation=hp['activation']))
model.add(Dropout(rate=hp['dropout']))
model.add(Dense(num_classes, activation='softmax'))

# 重新调整学习率
# model.compile(optimizer=Adam(learning_rate=1e-4), loss='categorical_crossentropy', metrics=['accuracy'])
optimizer = Adam(learning_rate=hp['learning_rate'])
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# 训练模型
# 初始化 TensorBoard 回调
# callbacks=[EarlyStopping(patience=5, restore_best_weights=True)] 用于在验证集性能不再提升时停止训练。
model.fit(x_train, y_train, epochs=hp['epochs'], batch_size=hp['batch_size'], validation_data=(x_test, y_test), callbacks=[tensorboard_callback, checkpoint_callback])

# 保存模型
model.save('my_model.keras')
joblib.dump(x_scaler, 'x_scaler.pkl')
joblib.dump(discretizer, 'discretizer.pkl')

# Test Accuracy: 6.83% 2025年3月7日 11:17:48
# Test Accuracy: 20.8054% 验证数据集（y_test）错误加工
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f"Test Loss: {test_loss:.4f}")
print(f"Test Accuracy: {round(test_accuracy * 100, 4)}%")

# 预测概率分布
# probabilities = model.predict(x_test)

# 转换为类别索引
# predicted_classes = np.argmax(probabilities, axis=1)
