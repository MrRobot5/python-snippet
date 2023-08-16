import requests

headers = {
    'app-token': 'noop',
    "accept": "*/*",
    "Content-Type": "application/json"
}

string = "tommy tang jimmy"


# 执行HTTP请求，将列表转换为字符串作为请求的主体
def send_http_request(foo):
    # 将列表转换为字符串
    data_string = "UPDATE `site_sales_info` SET `region_id`=423, `battle_id`=627 WHERE `sales_erp`='{}';".format(foo)

    # 发送HTTP请求，将data_string作为请求的body
    response = requests.post('http://foundation-pre.crm.foo.com/api/v1/test/DevTools/update/site_prod/1', headers=headers, data=data_string.encode())
    # 处理HTTP响应
    print(foo + " --- " + str(response.json()))


if __name__ == '__main__':
    words = string.split()

    for word in words:
        # 调用HTTP接口处理每个单词
        send_http_request(word)
