
"""
使用Prophet框架进行简单时间序列预测的示例代码
pip install prophet
https://facebook.github.io/prophet/docs/quick_start.html

@since 2024年12月30日 20:16:23

"""

import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('../candy/calls_data.csv')

# 重命名列, 符合Prophet的要求（`ds`为日期列，`y`为值列）。
# 在大多数机器学习项目中，术语y通常用于目标列（要测试的内容）。
data.rename(columns={'timestamp': 'ds', 'calls': 'y'}, inplace=True)

# 特性1：  添加假期效应，假期效应可以显著影响时间序列数据。
holidays = pd.DataFrame({
    'holiday': ['New Year\'s Day', 'Spring Festival', 'National Day'],
    'ds': pd.to_datetime(['2023-01-01', '2023-02-12', '2023-10-01']),
    'lower_window': 0,
    'upper_window': 1,
})

# 创建并训练模型
model = Prophet(holidays=holidays)
model.fit(data)

# 创建未来7天的数据框架并进行预测
future = model.make_future_dataframe(periods=7)

# 我们需要将预测数据从周末中删除。
future_boolean = future['ds'].map(lambda x : True if x.weekday() in range(0, 5) else False)
future = future[future_boolean]
forecast = model.predict(future)

# 查看预测结果
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# 绘制预测结果
# Prophet提供了两个方便的可视化助手，plot和plot_components。plot函数创建了实际/预测的图表，plot_components提供了趋势/季节性的图表。
fig = model.plot(forecast)
plt.show()