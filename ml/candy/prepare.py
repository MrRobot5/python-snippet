
"""
数据预处理（增加 target 列 "return"）
处理规则： 使用未来 5天的close - 当前close, 打标数据盈亏
    5天的数据对比，PnL 波动更加明显, 反之也更加灵敏

源数据： input.csv (basic/http/loop_fetch.py)

@since 2025年1月2日 17:35:39
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
df = df[df['timestamp'] > '2019-01-01'][:500]
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

# 输出到新的CSV文件
# 删除roll 移动n行, 最后 n 行 return不对，Mean Squared Error 从1.6 提升到 0.8 @since 2025年1月9日 13:28:38
# df[:-look_back].to_csv(output_filename, index=False)
df.to_csv(output_filename, index=False)
print(f"处理完成，结果已保存到 {output_filename}")