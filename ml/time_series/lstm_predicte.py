
"""
使用 LSTM （长短期记忆网络）进行数据序列预测。
pip install numpy pandas matplotlib tensorflow
@since
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 读取数据
data = pd.read_csv('../candy/calls_data.csv', parse_dates=['timestamp'], index_col='timestamp')
print(data.head())

# 提取调用量数据
calls_data = data['calls'].values.reshape(-1, 1)

# 数据标准化
scaler = MinMaxScaler(feature_range=(0, 1))
calls_data = scaler.fit_transform(calls_data)


# 创建训练和测试集
def create_dataset(data, time_step=1):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), 0]
        X.append(a)
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 10
X, y = create_dataset(calls_data, time_step)

# 重新调整输入数据的形状为 [samples, time steps, features]
X = X.reshape(X.shape[0], X.shape[1], 1)

# 分割数据集为训练集和测试集
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 构建和训练 LSTM 模型
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

model.summary()

# 训练模型
model.fit(X_train, y_train, batch_size=1, epochs=3)

# 使用训练好的模型进行预测
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# 反归一化数据
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
y_train = scaler.inverse_transform(y_train.reshape(-1, 1))
y_test = scaler.inverse_transform(y_test.reshape(-1, 1))


# 滚动预测未来5天的调用量
def predict_future(data, model, time_step, days):
    predictions = []
    last_data = data[-time_step:]

    for _ in range(days):
        pred = model.predict(last_data.reshape(1, time_step, 1))
        predictions.append(pred[0, 0])
        last_data = np.append(last_data[1:], pred)

    return np.array(predictions)


future_predictions = predict_future(calls_data, model, time_step, 5)
future_predictions = scaler.inverse_transform(future_predictions.reshape(-1, 1))

# 打印未来5天的预测结果
print("未来5天的调用量预测：")
print(future_predictions)

# 绘制结果
plt.figure(figsize=(12, 6))
plt.plot(scaler.inverse_transform(calls_data), label='Original Data')
plt.plot(np.arange(time_step, len(train_predict) + time_step), train_predict, label='Train Predict')
plt.plot(np.arange(len(train_predict) + (time_step * 2) + 1, len(calls_data) - 1), test_predict, label='Test Predict')

# 绘制未来5天预测结果
plt.plot(np.arange(len(calls_data), len(calls_data) + 5), future_predictions, label='Future Predict', marker='o')

plt.legend()
plt.show()