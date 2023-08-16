import requests

"""
批量刷新线上数据(特点： 批量提交 update SQL)。
@see mix_source_job.py 进阶版本
@since 2023-08-02 10:28:30
"""

headers = {
    'app-token': 'noop',
    "accept": "*/*",
    "Content-Type": "application/json"
}

# 创建一个空列表来存储待处理的字符串
data_list = []


def get_source_data(param):
    """
    加载远程数据。
    """
    data = {'visitId': param}
    response = requests.get("http://visit.crm.foo.com/newcrm/visitcenter/getVisitDetailById", headers=headers, params=data)
    return response.json().get("data")


def process_line(line, index):
    """
    使用chat-gpt 生成处理框架
    prompt: 我需要实现一个批量提交http请求功能，处理的字符串先 append 到 list，达到 200 条数据，再执行真正提交 http 请求，把 list 转为字符串作为 http body. 完成之后清空 list
    """
    # print(threading.current_thread())

    response = requests.get("http://site.foo.com/getUserPinInfo.json?jdPin=" + line, headers=headers)
    site = response.json().get("data")
    if not site:
        return
    if site.get("saleLineCode") not in ["KJBZ", "KJLLYY"]:
        return

    site.update({"index": index})

    sql = "UPDATE `site_visit` SET `sales_line`='{saleLineCode}' WHERE `id`={index};".format(**site)

    data_list.append(sql)
    print("data_list.append " + str(index))

    # 当列表中的元素数量达到 200 时，执行HTTP请求
    if len(data_list) == 200:
        send_http_request()
        # 清空列表
        data_list.clear()


# 执行HTTP请求，将列表转换为字符串作为请求的主体
def send_http_request():
    # 将列表转换为字符串
    data_string = '\n'.join(data_list)

    # 发送HTTP请求，将data_string作为请求的body
    response = requests.post('http://foundation-pre.crm.foo.com/api/v1/test/DevTools/update/site_prod/200', headers=headers, data=data_string.encode())
    # 处理HTTP响应
    print(response.json())


if __name__ == '__main__':
    for index in range(22412265, 20804185, -1):
        print(index)
        site = get_source_data(index)
        if not site:
            continue

        process_line(site.get("visitor"), index)
