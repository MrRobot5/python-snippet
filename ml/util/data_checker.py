"""
可视化显示 y_test 和 y_pred
背景：虽然 MSE 很小，通过可视化，发现 y_pred 数据区分度很低

源数据：test_predict.csv 训练完模型后，测试预测结果

@see data_plot.py
@since 2025年2月26日
"""
import pandas as pd
from sklearn.metrics import mean_squared_error

# 真正的均方误差小的示例
data = pd.read_csv('predict_check_fake.csv')  # 替换为你的 CSV 文件路径[^4^]

# 提取 original 和 scaled 列
y_test = data['y_test']  # 假设列名为 'original'
y_pred = data['y_pred']  # 假设列名为 'scaled'

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)

# MSE of prediction for test set is: 0.0002% 👍
print(f'MSE of prediction for test set is: {round(mse * 100, 4)}%')
