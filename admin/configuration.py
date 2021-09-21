from datetime import timedelta

class Configuration ( ):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/election"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = "localhost"
    REDIS_VOTES_LIST = "votes"
    REDIS_CHAN = "newVotes"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta ( minutes = 180 )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta ( days = 30 )
