import redis
import time

def generateData():
    print "generate"
    time.sleep(1)
    return "404"

# redis read-through cache
conn = redis.Redis()

def get(key):
    recache = 2
    data = conn.get(key)
    ttl = conn.ttl(key)

    if ttl < recache and conn.setnx('lock:' + key, 'locked'):
        print 'recache'
        # long-running process
        data = generateData()
        conn.setex(key, data, 10)
        conn.delete('lock:' + key)
    # normal return
    return data

print get("xxxxxx")