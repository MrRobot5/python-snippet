from sklearn.preprocessing import LabelEncoder
le = LabelEncoder() # 创建一个LabelEncoder对象
le.fit([1, 2, 2, 6]) # 将编码器拟合到给定的类别
print(le.classes_) # 显示拟合后的类别（unique）
le.transform([1, 1, 2, 6]) # 将给定的类别转换为整数
le.inverse_transform([0, 0, 1, 2]) # 将整数逆转换回原始类别
