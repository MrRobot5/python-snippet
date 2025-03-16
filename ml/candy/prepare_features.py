
"""
数据预处理（特征工程）


源数据： input.csv (basic/http/loop_fetch.py)

@since 2025年3月16日 10:21:55
"""

import numpy as np
import pandas as pd

# 读取CSV文件
input_filename = 'input.csv'
output_filename = 'train.csv'

# PnL 验证天数（使用5天来训练2019-01-02 00:00:00 ~ 2021-01-20 00:00:00， 预测2022-01 的数据，效果很好）
look_back = 5

# 使用pandas读取CSV文件
df = pd.read_csv(input_filename, parse_dates=['timestamp'])
column_names_list = df.columns.tolist()
print(column_names_list)

# 将timestamp列转换为datetime类型
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# 按照 timestamp 列的值进行升序排序
df.sort_values(by='timestamp', ascending=True, inplace=True)

# 过滤timestamp大于'2022-01-01'的数据
# 预测简单的周期性数据或趋势较为明显的数据，可能几千条到几万条数据就可以构建一个效果不错的 LSTM 模型。
df = df[df['timestamp'] > '2010-01-01'][:3000]
print(df.head(10))
min_ts = df['timestamp'].min()
max_ts = df['timestamp'].max()
print(f"时间戳范围: {min_ts} ~ {max_ts}")

# 计算的是未来 look_back 行的值与当前行值的差，即未来价格与当前价格的差额。
# 上述差额除以当前行的值，计算的是收益率（或变化率）。@since 2025年3月9日， 使用百分比替换绝对值，防止未来几年由于价格上涨，导致用之前的结果误判涨幅。
# 使用shift方法直接计算差值，避免循环
# for i in range(0, df.shape[0] - look_back):  # disgard the last "look_back" days
#     result.append(df.iloc[i + look_back]['close'] - df.iloc[i]['close'])
df['return'] = (df['close'].shift(-look_back) - df['close']) / df['close']

# 删除最后look_back行的NaN值（因为shift操作会引入NaN）
df = df.dropna(subset=['return'])

# 计算MACD指标
# fast=12、slow=26、signal=9：分别为 MACD 的快速、慢速和信号线的平滑参数。
# append=True：将计算结果直接添加到原始 DataFrame 中。
df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

# 输出结果
df.to_csv(output_filename, index=False)
print(f"MACD指标已计算完成，并保存到文件：{output_filename}")

# 输出到新的CSV文件
# 删除roll 移动n行, 最后 n 行 return不对，Mean Squared Error 从1.6 提升到 0.8 @since 2025年1月9日 13:28:38
# df[:-look_back].to_csv(output_filename, index=False)
df.to_csv(output_filename, index=False)
print(f"处理完成，结果已保存到 {output_filename}")