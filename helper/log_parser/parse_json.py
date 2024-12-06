"""
从日志文件中提取 json 字符串中的"id" 值
@since 2024年12月6日 13:55:09
"""

import json
import re
from log_utils import get_latest_log_file, save_ids_to_file

def extract_ids_from_log(file_path):
    ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 使用正则表达式提取 JSON 部分
            match = re.search(r'\{.*\}', line)
            if match:
                json_str = match.group(0)
                try:
                    data = json.loads(json_str)
                    if 'id' in data:
                        ids.append(data['id'])
                except json.JSONDecodeError:
                    # 跳过无法解析的行
                    continue
    return ids


directory = 'c:/Users/yangpan3/Downloads/'
latest_log_file = get_latest_log_file(directory)
if latest_log_file:
    print(f"Latest log file: {latest_log_file}")
    extracted_ids = extract_ids_from_log(directory + latest_log_file)
    print(extracted_ids)

    # 将 extracted_ids 结果输出到 txt 文件中
    save_ids_to_file(extracted_ids, 'extracted_ids.txt')
else:
    print("No .log files found in the directory.")