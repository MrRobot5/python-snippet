from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

# 加载示例数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 拆分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 创建 SVC 模型并训练
model = SVC(kernel='linear')  # 指定核函数为线性核
model.fit(X_train, y_train)

# 预测
predictions = model.predict(X_test)
print(predictions)