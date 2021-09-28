from datetime import timedelta
import os

redisHost = os.environ["REDIS_HOST"]
class Configuration ( ):
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = redisHost
    REDIS_VOTES_LIST = "votes"
    REDIS_CHAN = "newVotes"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 180 )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 )
