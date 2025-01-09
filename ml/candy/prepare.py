
"""
数据预处理（增加 target 列）
处理规则： 使用未来3天的close - 当前close, 打标数据盈亏
源数据： input.csv

@since 2025年1月2日 17:35:39
"""


import numpy as np
import pandas as pd

# 读取CSV文件
input_filename = 'input.csv'
output_filename = 'train.csv'

# 使用pandas读取CSV文件
df = pd.read_csv(input_filename, parse_dates=['timestamp'])
# 将timestamp列转换为datetime类型
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# 按照 timestamp 列的值进行升序排序
df.sort_values(by='timestamp', ascending=True, inplace=True)

# 过滤timestamp大于'2022-01-01'的数据
df = df[df['timestamp'] > '2022-01-01']
print(df.head(10))

look_back = 3
# 计算i+n行减去i行的“close”
# 使用np.roll函数将“close”列向下移动n行，然后与原始列相减
df['target'] = np.roll(df['close'],  - look_back) - df['close']

# 删除target列为NaN的行
# 由于np.roll会导致前5行的target列为NaN，我们可以将这些值替换为一个特定的值或删除这些行
# df = df.dropna(subset=['target'])

# 输出到新的CSV文件
# 删除roll 移动n行, 打标不对，Mean Squared Error 从1.6 提升到 0.8 @since 2025年1月9日 13:28:38
df[:-look_back].to_csv(output_filename, index=False)

print(f"处理完成，结果已保存到 {output_filename}")