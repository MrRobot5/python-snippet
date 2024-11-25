import threading
import time
import random


# 定义一个函数，用于在线程中执行
def worker(num):
    print('线程 %s 开始执行' % num)
    time.sleep(10 * random.random())


if __name__ == '__main__':
    # 创建 5 个线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)

    # 启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程执行完毕
    for t in threads:
        t.join()

    print('所有线程执行完毕')
