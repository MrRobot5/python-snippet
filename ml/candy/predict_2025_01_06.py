"""
利用已经训练好的模型，预测验证
源数据： input.csv

@since 2025年1月6日 17:36:38
"""
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# 读取CSV文件
df = pd.read_csv('input.csv', parse_dates=['timestamp'])

df = df[df['timestamp'] > '2022-03-01'][:90]
print(df.head(10))
data = df.drop(['id', 'timestamp'], axis=1)

# 假设最后一列为target，其他列为特征
# 将DataFrame转换为数组: 使用.values属性将DataFrame转换为NumPy数组
features = data.iloc[:, :].values

# 数据归一化
scaler = MinMaxScaler(feature_range=(0, 1))
features_scaled = scaler.fit_transform(features)

features_tf = np.reshape(features_scaled, (features_scaled.shape[0], 1, features_scaled.shape[1]))

# 加载模型
loaded_model = load_model('my_model.h5')

# 进行预测
# 使用加载的模型进行预测或评估
predictions = loaded_model.predict(features_tf)

# 导出数据和预测结果到 csv
# 将数组转换回DataFrame: 使用pd.DataFrame()构造函数将数组转换回DataFrame
# since 2025年1月6日 16:09:23
original_test = pd.DataFrame(features_scaled, columns=data.columns)
original_test["pred"] = predictions
original_test.to_csv('predict.csv', index=False)

