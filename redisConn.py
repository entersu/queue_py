import sys
import redis
class redisConn:
    __instance = None
    redis = None

    def __new__(self):
        if self.__instance:
            return self.__instance
        self.__instance = object.__new__(self)
        self.__instance.__setConnent("localhost", 6379, 1)
        return self.__instance

    def __setConnent(self, host, port, db):
        pool = redis.ConnectionPool(host=host, port=port, db=db)
        self.redis = redis.StrictRedis(connection_pool=pool)
        # self.redis = redis.Redis(host=host, port=port, db=db)
        return self.redis

    def getInstance(self):
        return self.__instance.redis

    def clear(self, error):
        print(__file__,sys._getframe().f_lineno,error)
        self.__instance.__setConnent("localhost", 6379, 1)