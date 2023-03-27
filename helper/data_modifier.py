# -*- coding: utf-8 -*-
"""
根据excel to json, 拼接需要调整的 sql
@since 2023-03-16 14:56:45
"""
import json

if __name__ == '__main__':
    with open('FeHelper-20230316150541.json', 'r', encoding='UTF-8') as f:
        json_text = f.read()
    data = json.loads(json_text)
    print("--total: {}".format(len(data)))
    for item in data:
        variable = json.loads(item["variable"])
        print("UPDATE `spm_jm_message` SET `business_no`='{}' WHERE `id`= {};".format(variable["requestId"], item["id"]))

