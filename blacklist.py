# Requires Redis server to be running.
import os

import redis

from datetime import timedelta

# Values can be changed.
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

# Setup the redis connection for storing the blacklisted tokens
revoked_store = redis.StrictRedis(host=os.environ.get('REDIS_URL'), port=6379, db=0, decode_responses=True)