import matplotlib.pyplot as plt
import pandas as pd
import json

"""
加班报销费用图表可视化

prompt: 给定json 数据如下，需求：applyTime 作为横坐标，按照月度显示，amount 作为纵坐标，制作不同年份的折线对比图。
2021年之前的数据不做显示
marker 显示具体的amount
data 数据改为从json 文件读取

@author chat-gpt
@since 2024年5月21日 16:54:23
"""


# Assuming your JSON data is stored in a file called 'data.json'
with open('data.json', 'r', encoding='utf-8') as f:
    data_json = json.load(f)

# Extract the relevant data from JSON
data = data_json['data']['myBill']['data']

# Normalize the data and read it into a pandas DataFrame
df = pd.json_normalize(data)

# Convert applyTime from Unix timestamp to datetime
df['applyTime'] = pd.to_datetime(df['applyTime'], unit='ms')

# Extract year and month for grouping
df['year'] = df['applyTime'].dt.year
df['month'] = df['applyTime'].dt.month

# Filter out data before 2021
df = df[df['year'] >= 2021]

# Group by year and month, and sum amounts for each group
grouped = df.groupby(['year', 'month'])['amount'].sum().reset_index()

# Pivot the DataFrame to have years as columns and months as rows
pivot_df = grouped.pivot("month", "year", "amount")

# Plotting
fig, ax = plt.subplots(figsize=(12, 6))
pivot_df.plot(ax=ax, marker='o')

# Show the amount on each marker
for i, line in enumerate(ax.get_lines()):
    for x_value, y_value in zip(line.get_xdata(), line.get_ydata()):
        label = "{:.2f}".format(y_value)
        ax.annotate(label,  # this is the text
                    (x_value, y_value),  # these are the coordinates to position the label
                    textcoords="offset points",  # how to position the text
                    xytext=(0,10),  # distance from text to points (x,y)
                    ha='center')  # horizontal alignment can be left, right or center


# Formatting the plot
ax.set_title('Monthly Amount Comparison Across Years', fontsize=16)
ax.set_xlabel('Month', fontsize=14)
ax.set_ylabel('Amount', fontsize=14)
ax.grid(True)
ax.legend(title='Year')

plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.show()
