import redis
from os import getenv
from flask_jwt_extended import get_jwt
from datetime import timedelta

redis_host = getenv('REDIS_HOST')
if redis_host is None:
    redis_host = 'redis'

jwt_redis_denylist = redis.StrictRedis(
    host=redis_host, port=6379, db=0, decode_responses=True
)


def add_jwt_to_denylist():
    jti = get_jwt()["jti"]
    jwt_redis_denylist.set(jti, "", ex=timedelta(minutes=1))

