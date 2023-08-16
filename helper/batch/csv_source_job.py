import csv
import requests

"""
根据线上导出的 csv 源文件，匹配对应的数据并批量更新。
"""

headers = {
    'lop-pin': 'foo',
    'LOP-DN': '*/*',
    'accept': '*/*',
    'Content-Type': 'application/json',
}


def get_source_data(param):
    """
    加载远程数据。
    """
    response = requests.get("http://ha.foo.com/api/foo/getBySiteCode/" + param, headers=headers)
    return response.json()


def send_http_request(site):
    """
    发起数据 update SQL
    @param site: json 格式
    """
    data = "UPDATE `site` SET `site_code`='{c1}', `site_name`='{c2}' WHERE  `id`='{c3}';".format(**site)
    # data.encode() 解决包含中文字符串的问题
    response = requests.post('http://c.foo.com/api/v1/update/sql/' + site.get("lines"), headers=headers, data=data.encode())
    print(response.json())


def process_line(row):
    site_code_ = row['site_code']
    source = get_source_data(site_code_)
    data = source["data"]
    if not data.get("siteName"):
        return

    siteName = data.get("siteName")
    siteCode = data.get("siteCode")
    send_http_request({"c1": siteCode, "c2": siteName, "c3": site_code_, "lines": row['count(*)']})


if __name__ == '__main__':
    with open('明细表_20230529152741.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['count(*)'], row['site_code'])
            process_line(row)
