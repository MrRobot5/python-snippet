"""
运行数据导出，方便分析和单独可视化

运行时数据导出：
pd.DataFrame(y_train).to_csv("original_y_train.csv", index=False, header=False)
pd.DataFrame(y_train).to_csv("scaled_y_train.csv", index=False, header=False)
pd.DataFrame(scaler2.inverse_transform(y_train)).to_csv("scaled_revert_y_train.csv", index=False, header=False)

@since 2025年2月26日
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# 示例数据：NumPy 数组
y_test = np.array([3, 2.5, 4, 3.5])
y_pred = np.array([3.1, 2.4, 4.1, 3.6])

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)

# 创建一个 DataFrame，包含 y_test 和 y_pred 的值
result_df = pd.DataFrame({
    'y_test': y_test,  # NumPy 数组直接传递给 DataFrame
    'y_pred': y_pred
})

# 添加 MSE 作为单独的一列（可选）
result_df['MSE'] = mse  # MSE 是标量，会自动广播到每一行

# 导出为 CSV 文件
result_df.to_csv('results.csv', index=False)

print("y_test、y_pred 和 MSE 已保存到 results.csv 文件中。")