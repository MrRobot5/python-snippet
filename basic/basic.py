# encoding: utf-8

import time


def range_test():
    for index in range(10000, 20000):
        print(str(index) + "s")
        time.sleep(0.1)


if __name__ == '__main__':
    range_test()
