
"""
使用shap来解释模型的预测。
SHAP值是一种基于博弈论的方法，用于量化每个特征对模型预测的贡献。

pip uninstall shap
pip install shap==0.41.0

pip show tensorflow
    Name: tensorflow
    Version: 2.15.0

@since 2025年2月19日 15:54:02
"""

import shap
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# 加载Iris数据集
iris = load_iris()
X = iris.data
y = iris.target

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练决策树模型
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# 初始化SHAP解释器
explainer = shap.Explainer(clf, X_train)

# 计算SHAP值（对于测试集）
shap_values = explainer(X_test)

# 可视化SHAP值（决策图）
shap.decision_plot(shap_values, features=X_test)

# 可视化SHAP值（摘要图）
shap.summary_plot(shap_values, X_test)
