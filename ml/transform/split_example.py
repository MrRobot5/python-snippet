
from sklearn.model_selection import train_test_split
import numpy as np

# 假设我们有一些数据和标签
X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
y = np.array([0, 1, 0, 1, 0, 1])

# 使用 train_test_split 函数拆分数据集
# test_size=0.2 表示测试集占总数据的 20%
# random_state=42 用于确保结果的可重复性
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 打印结果
print("X_train:\n", X_train)
print("y_train:\n", y_train)
print("X_test:\n", X_test)
print("y_test:\n", y_test)
