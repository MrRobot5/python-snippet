"""
利用已经训练好的模型，预测验证
源数据： input.csv

@since 2025年1月6日 17:36:38
"""
import numpy as np
import pandas as pd
import joblib
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

output_filename = 'predict.csv'

# 读取CSV文件
df_test = pd.read_csv('input.csv', parse_dates=['timestamp'])
df_test.sort_values(by='timestamp', ascending=True, inplace=True)

# 选取与 train.csv 无交集的数据
df_test = df_test[df_test['timestamp'] > '2022-01-01'][:85]
print(df_test.head(10))

selected_columns = ["volume", "open", "high", "low", "close", "turnoverrate"]
# selected_columns = ['volume', 'open', 'high', 'low', 'close', 'chg', 'percent', 'turnoverrate', 'amount', 'pe', 'pb', 'ps', 'pcf', 'market_capital']

# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
df_feature_test = df_test.loc[:, selected_columns].copy().values

timestep = 10 # use days to predict next 1 day return

# 数据归一化
# fix: 使用trian 归一化fit， 保持transform 结果一致 2025年2月26日 10:37:39
# scaler = MinMaxScaler(feature_range=(0, 1))
scaler = joblib.load('minmax_scaler.pkl')
df_feature_test = scaler.transform(df_feature_test)

x_test = []
for i in range(timestep, df_feature_test.shape[0]):  # discard the last "timestep" days
    x_test.append(df_feature_test[i - timestep:i])  # rolling_timestep * features

x_test = np.array(x_test) # days * timestep * features

# 加载模型
loaded_model = load_model('my_model.h5')

# 进行预测
# 使用加载的模型进行预测或评估
predictions = loaded_model.predict(x_test)

# 导出数据和预测结果到 csv
# 将数组转换回DataFrame: 使用pd.DataFrame()构造函数将数组转换回DataFrame
# since 2025年1月6日 16:09:23
original_test = pd.DataFrame(df_feature_test[timestep:], columns=selected_columns)
original_test["pred"] = predictions
original_test.to_csv(output_filename, index=False)

print(f"处理完成，结果已保存到 {output_filename}")

