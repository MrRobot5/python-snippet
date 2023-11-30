import redis

conn = redis.Redis()


def list_test():
    conn.rpush("list-key", "1")
    conn.rpush("list-key", "2")
    conn.lpush("list-key", "3")
    rs = conn.lrange("list-key", 0, -1)
    print(rs)


if __name__ == '__main__':
    list_test()
