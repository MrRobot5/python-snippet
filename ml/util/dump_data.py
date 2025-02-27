"""
sqlite 数据导出为csv 文件
场景：循环抓取数据，使用 sqlite 存储更加方便实现。训练模型为了可视化，csv 更加方便。需要中间转换。

@see loop_fetch.py
"""

import pandas as pd
from sqlalchemy import create_engine

# 创建数据库连接
engine = create_engine("sqlite:///database_SZ000625.db", pool_recycle=3600, echo=True)

# 查询特定列的数据
query = "SELECT * FROM kline_data order by timestamp asc;"  # 假设表名为 kline_data
data = pd.read_sql(query, con=engine)

# 将数据保存为 CSV 文件
data.to_csv("kline_data.csv", index=False)  # index=False 表示不保存索引列

print("数据已成功导出到 kline_data.csv 文件中。")
