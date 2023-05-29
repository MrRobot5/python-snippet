
"""
解析 url 中的username 信息
"""
if __name__ == '__main__':
    foo = "https://wenku.baidu.com:.@:com@/sites/SXHT"

    index = foo.find("://")
    protocol = foo[:index]
    print(protocol)
    tmp = foo[index + 3:]
    print(tmp)
    index = tmp.rfind("@")
    userPart = tmp[:index]
    print(userPart)
    index = userPart.find(":")
    print(userPart[: index])
    print(userPart[index + 1:])




