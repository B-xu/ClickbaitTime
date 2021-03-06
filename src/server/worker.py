import os

import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)
# conn = redis.Redis('localhost', 6379, 0)

if __name__ == '__main__':
    with Connection(conn):
        print('Worker started')
        worker = Worker(list(map(Queue, listen)))
        worker.work()