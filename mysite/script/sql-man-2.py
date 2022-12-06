# -*- coding:utf-8 -*-

# 生成批量删除的脚本

total = 0
while total < 61880350:
    total += 1000000
    print "delete from sha_pin_new where id < {};".format(total)




