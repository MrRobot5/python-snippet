
"""
根据接口调用量趋势预测未来5天趋势 （日期列仅作为普通数据列处理）
使用 sklearn 进行简单的时间序列预测。当然，对于更复杂的时间序列预测任务，可能需要更复杂的模型和方法，如 ARIMA、LSTM 等。

@since 2024年12月30日 17:17:38
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# 1. 读取数据
df = pd.read_csv('calls_data.csv')

# 2. 将 timestamp 转换为 datetime 类型，并创建天数列
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['days'] = (df['timestamp'] - df['timestamp'].min()).dt.days + 1

# 3. 准备数据
days = df['days'].values.reshape(-1, 1)
calls = df['calls'].values

# 4. 创建并拟合模型
model = LinearRegression()
# 根据日期（入参） 和 调用量（结果）的关系，拟合计算公式
model.fit(days, calls)

# 5. 预测接下来5天的调用量
last_day = df['days'].max()
future_days = np.array([last_day + i for i in range(1, 6)]).reshape(-1, 1)
predicted_calls = model.predict(future_days)

# 6. 创建预测的时间戳
last_timestamp = df['timestamp'].max()
future_timestamps = [last_timestamp + timedelta(days=i) for i in range(1, 6)]

# 7. 输出预测结果
print("预测的接下来5天的调用量: ", predicted_calls)

# 8. 可视化结果
plt.figure(figsize=(10, 6))
plt.scatter(df['timestamp'], df['calls'], color='blue', label='真实数据')
plt.plot(df['timestamp'], model.predict(days), color='green', label='拟合曲线')
plt.scatter(future_timestamps, predicted_calls, color='red', label='预测数据')
plt.plot(future_timestamps, predicted_calls, color='orange', linestyle='dashed', label='预测趋势')

plt.xlabel('日期')
plt.ylabel('调用量')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()