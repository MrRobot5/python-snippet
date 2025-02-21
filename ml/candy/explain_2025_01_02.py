"""
评估模型中各特征的重要性
首先是特征重要性分析，可以使用SHAP或LIME这样的工具来解释模型的预测结果。
其次，可以考虑对模型的权重进行分析，看看哪些输入特征对模型决策影响最大
源数据： train.csv

@since 2025年2月19日 14:05:18
@see train_2025_01_02.py 参考模型
"""
import shap
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt


# 训练模型
# model.fit(X_train_tf, y_train, epochs=80, batch_size=8, validation_data=(X_test_tf, y_test))

model = load_model('my_model.h5')

# 计算 SHAP 值
# SHAP库本身并不直接支持LSTM模型的解释，因为LSTM模型的内部状态和时间依赖性使得标准的特征重要性计算方法不再适用。
# explainer = shap.DeepExplainer(model, X_train_tf[:100])  # X_train 是训练数据
# shap_values = explainer.shap_values(X_test_tf)

# 可视化特征重要性
# shap.summary_plot(shap_values, X_test_tf)


# 输出模型权重
# 获取 LSTM 层的权重
lstm_layer = model.layers[0]
weights = lstm_layer.get_weights()

# 假设输入特征数为 `input_features`
input_weights = weights[0]  # 输入到遗忘门、输入门、输出门的权重
feature_importance = np.mean(np.abs(input_weights), axis=1)

# 获取列名数组
# feature_names = data.columns.values  # 转换为 numpy 数组
# print(feature_names)
feature_names = ["volume", "open", "high", "low", "close", "turnoverrate"]

# 将特征重要性排序
sorted_features = np.argsort(feature_importance)[::-1]
sorted_feature_names = [feature_names[i] for i in sorted_features]
sorted_feature_importance = feature_importance[sorted_features]
# 特征排序: ['volume', 'low', 'high', 'close', 'open']
# 特征重要性: [0.19977868 0.12423202 0.11919323 0.11911967 0.10971662]
print("特征排序:", sorted_feature_names)
print("特征重要性:", feature_importance[sorted_features])

# 可视化特征贡献
# 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(range(len(sorted_feature_names)), sorted_feature_importance, tick_label=sorted_feature_names)
plt.title("特征重要性排序")
plt.xlabel("特征")
plt.ylabel("重要性")
plt.xticks(rotation=45)
plt.show()