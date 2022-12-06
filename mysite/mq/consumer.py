# -*- coding:utf-8 -*-

import stomp
import time
# 推送到主题
__topic_name1 = '/topic/FirstTopic'
__topic_name2 = '/topic/SecondTopic'
__host = '127.0.0.1'
__port = 61613
__user = 'manbuzhe'
__password = '20180725'

def send_to_topic(topic, msg):

    if topic == 1:
        conn.send(__topic_name1, msg)
    else:
        conn.send(__topic_name2, msg)


if __name__ == '__main__':
    conn = stomp.Connection10([(__host, __port)])
    conn.start()
    conn.connect(__user, __password, wait=True)
    for i in range(10):
        send_to_topic(1, 'topic1: 测试信息1...')
        send_to_topic(2, 'topic2: 测试信息2...')
        time.sleep(5)
    conn.disconnect()