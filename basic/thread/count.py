import time
import threading
import random

"""
python 创建线程、异步运行示例
"""

thread_num = 10


def run():
    """
    类似 Java Runnable
    """
    print('start, there are', threading.activeCount(), 'threads running')
    time.sleep(10 * random.random())
    print('finish, there are ', threading.activeCount(), 'threads running')


if __name__ == '__main__':
    for i in range(thread_num):
        th = threading.Thread(target=run)
        th.start()
