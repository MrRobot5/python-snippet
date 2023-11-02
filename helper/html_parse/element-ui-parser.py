# -*- coding:utf-8 -*-

"""

@author chat-gpt
@since 2023年11月2日19:43:16
"""

from bs4 import BeautifulSoup

"""你的HTML代码"""
html = """

<el-table :data="list">
      <el-table-column label="创建日期" prop="createTime" align="center">
        <template slot-scope="scope">
          {{ new Date(scope.row.createTime).toISOString().split("T")[0] }}
        </template>
      </el-table-column>
      <el-table-column label="收入倍差" prop="incomeFactor" align="center"></el-table-column>
      <el-table-column label="价格倍差" prop="priceFactor" align="center"></el-table-column>
      <el-table-column label="客户数" prop="customerCount" align="center"></el-table-column>
    </el-table>

"""

soup = BeautifulSoup(html, 'html.parser')

labels = []
props = []

for column in soup.find_all('el-table-column'):
    labels.append(column.get('label'))
    prop = column.get('prop')
    if not prop:
        props.append("")
    else:
        props.append(prop)

print("\t".join(labels))
print("\t".join(props))
