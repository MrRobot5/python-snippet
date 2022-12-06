import threading
import time
import redis

conn = redis.Redis()

def publisher(n):
    time.sleep(1)
    for i in xrange(n):
        conn.publish('channel', i)
        # After publishing, we'll pause for a moment so that we can see this happen over time
        time.sleep(1)

def run_pubsub():
    # Let's start the publisher thread to send three messages.
    threading.Thread(target=publisher, args=(3,)).start()
    pubsub = conn.pubsub()
    pubsub.subscribe(['channel'])
    count = 0
    # we can listen to subscription messages by iterating over the result of pubsub.listen()
    for item in pubsub.listen():
        print item
        count += 1
        if count == 4:
            pubsub.unsubscribe()
        if count == 5:
            break
# Actually run the functions to see them work
run_pubsub()