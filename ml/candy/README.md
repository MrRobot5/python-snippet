
## 数据
源数据： input.csv
训练数据： train.csv
模型：my_model.h5

## 功能模块
准备训练数据： prepare.py
训练模型： train_2025_01_02.py
模型预测：predict_2025_01_06.py
可视化验证: ta_chart_2025_01_06.py

## usage
1. prepare.py 处理源数据，增加打标 target 列
2. train_2025_01_02.py 根据打标过的数据 train.csv,  训练模型
3. predict_2025_01_06.py 使用模型验证历史的数据 Trend 或者预期未来的Trend
4. ta_chart_2025_01_06.py 指标可视化，和经典的指标相互对比
