# encoding: utf-8

import time
import os


def range_test():
    for index in range(10000, 20000):
        print(str(index) + "s")
        time.sleep(0.1)


def time_format():
    ti_m = os.path.getmtime('basic.py')

    m_ti = time.ctime(ti_m)

    # Using the timestamp string to create a
    # time object/structure
    t_obj = time.strptime(m_ti)

    # Transforming the time object to a timestamp
    # of ISO 8601 format
    T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)

    print("The file located at the path {} was last modified at {}".format('basic.py', T_stamp))


if __name__ == '__main__':
    # range_test()
    time_format()
    title = "h2database BTree 设计实现与查询优化思考"
    print(title.split(" "))
