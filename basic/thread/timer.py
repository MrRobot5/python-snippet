# -*- coding:utf-8 -*-

import threading


def func1(a):
    # Do something
    print(str(threading.currentThread()) + 'Do something')
    a += 1
    print(a)
    print('当前线程数为{}'.format(threading.activeCount()))
    if a > 5:
        return
    t = threading.Timer(5, func1, (a,))
    t.start()


if __name__ == '__main__':
    func1(0)
