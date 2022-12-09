# -*- coding:utf-8 -*-

"""
批量查询 mysql table 数据量
特殊功能： sql format
依赖： pip install sqlparse
2022年09月07日 16:54:22
"""
import sqlparse


tables = "spm_chance_share_pool spm_chance_share_pool_rule spm_chance_share_pool_special_depart spm_company_chance_contract_product_rel spm_company_chance_rel spm_chance_offer_file_rel spm_chance_offer_rel spm_chance_pool".split(" ")
result = []
for table in tables:
    result.append("select '{0}' as name, count(*) from {0} where is_delete = 0".format(table))

sql = " union all ".join(result)
print(sqlparse.format(sql, reindent=True, keyword_case='upper'))
