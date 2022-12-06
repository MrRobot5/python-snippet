# -*- coding:utf-8 -*-

# see String 7.1.3.2. Format examples

if __name__=='__main__':
    brandId = ""
    brandName = ""
    with open("C:\\Users\\yangpan3\\Desktop\\append.txt") as f:
        for line in f:
            items = line.split(":")
            if len(items) < 2:
                continue
            brandId += items[0].strip() + ','
            brandName += items[1].replace('\n', '').strip() + ','

    brandId = brandId[0: len(brandId) - 1]
    print(brandId)
    brandName = brandName[0: len(brandName) - 1]
    print(brandName)
    print('--生成sql--')
    print(
        "update user_info set brand_id_string='{}', brand_name_string='{}', update_time=now() where pin = 'test_9n';".format(
            brandId, brandName))

