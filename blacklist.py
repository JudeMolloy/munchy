# Requires Redis server to be running.
import os
import redis

from urllib.parse import urlparse
from datetime import timedelta

# Values can be changed.
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)

#url = urlparse(os.environ.get("REDIS_URL"))
#revoked_store = redis.StrictRedis(host=url.hostname, port=url.port, username=url.username, password=url.password, ssl=True, ssl_cert_reqs=None)

# Setup the redis connection for storing the blacklisted tokens
env = os.environ.get("CONFIG_ENV")

if env == "config.DevelopmentConfig":
    revoked_store = redis.StrictRedis(host=os.environ.get('REDIS_URL'), port=6379, db=0, decode_responses=True)
else:
    revoked_store = redis.from_url(os.environ.get("REDIS_URL"))
#revoked_store = redis.Redis(host=os.environ.get('REDIS_URL'))
#revoked_store = redis.StrictRedis(host=os.environ.get('REDIS_URL'), port=6379, db=0, decode_responses=True)