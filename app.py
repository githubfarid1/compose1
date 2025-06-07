import time

import redis
from flask import Flask
from pytz import timezone
from datetime import datetime
app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    today = datetime.now(timezone("Asia/Jayapura")).strftime("%Y-%m-%d")
    count = get_hit_count()
    return f'Hello Farid! I have been seen {count} times. today is {today}\n'