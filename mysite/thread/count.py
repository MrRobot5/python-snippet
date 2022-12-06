import time
import threading
import random
thread_num = 10


def run():
    print('first, there are', threading.activeCount(), 'threads running')
    time.sleep(10 * random.random())
    print('second, there are ', threading.activeCount(), 'threads running')

for i in range(thread_num):
    th = threading.Thread(target = run)
    th.start()