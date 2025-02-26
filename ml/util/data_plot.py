"""
可视化显示 y_test 和 y_pred
背景：虽然 MSE 很小，通过可视化，发现 y_pred 数据区分度很低

源数据：test_predict.csv 训练完模型后，测试预测结果

@since 2025年2月26日
"""

import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
data = pd.read_csv('test_predict.csv')  # 替换为你的 CSV 文件路径[^4^]

# 提取 original 和 scaled 列
y_test = data['y_test']  # 假设列名为 'original'
y_pred = data['y_pred']  # 假设列名为 'scaled'

# 绘制折线图
plt.plot(y_test, label='y_test', marker='o')  # 添加标记以便更清晰[^2^]
plt.plot(y_pred, label='y_pred', marker='x')     # 添加标记以便更清晰[^2^]

# 添加标题和标签
plt.title('Original vs Scaled Values')
plt.xlabel('Index')
plt.ylabel('Value')
plt.legend()  # 添加图例[^3^]

# 显示图表
plt.show()
