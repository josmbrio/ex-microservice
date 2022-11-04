import redis
from os import getenv

redis_host = getenv('REDIS_HOST')
if redis_host is None:
    redis_host = 'redis'

print("Redis host: " + redis_host)
jwt_redis_denylist = redis.StrictRedis(
    host=redis_host, port=6379, db=0, decode_responses=True
)

