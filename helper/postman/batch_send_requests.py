"""
批量发起请求并记录请求结果到 Excel
template
@since 2024年12月27日 11:34:29
"""

import pandas as pd
import requests

# 读取 Excel 文件
file_path = 'request.xlsx'
sheet1 = pd.read_excel(file_path, sheet_name='Sheet1')

# 存储结果的列表
results = []

# 遍历每一行，根据 "实物流id" 发起请求
for index, row in sheet1.iterrows():
    bill_id = row['业务单号']

    # 发起请求
    response = requests.get(
        'http://yf.lrl.foo.com/some/manual.do',
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        },
        params={'ldId': bill_id},
        verify=False
    )

    # 解析响应
    response_data = response.json()
    print(response_data)
    if response_data.get("success"):
        results.append({
            '业务单号': bill_id,
            '结果': '成功'
        })
    else:
        results.append({
            '业务单号': bill_id,
            '结果': response_data.get("tipMsg", "未知错误")
        })

# 将结果转为 DataFrame 并写入 Excel
results_df = pd.DataFrame(results)
results_df.to_excel('request_results.xlsx', index=False)

print('请求结果已保存到 request_results.xlsx')