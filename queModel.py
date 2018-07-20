import hashlib
import json
import time
from base import baseModel
from dbConn import dbConn
from redisConn import redisConn
import sys
class queModel(baseModel):
    steps = {'0':0,'1':5,'2':15,'3':15,'4':30,'5':180,'6':1800,'7':1800,'8':3600}
    notify_queue_num = 2
    queue_prefix = "notify_queue_"
    queue_tmp_bak = "notify_queue_bak_"
    queue_val_split = "|"

    def getInstance(self):
        return super(queModel, self).getInstance(self.__class__);

    def splicing(self, order_no, pay_time, step):
        return '%s|%s|%s' % (order_no, pay_time, step)

    def getQueueDesBlock(self, redis_key, redis_des_key, second = 0):
        result = redisConn().getInstance().brpoplpush(redis_key, redis_des_key, second)
        return result

    def repushQueue(self, order_no, pay_time, count):
        value = self.splicing(order_no, pay_time, count)
        key = self.__getPayRedisKey(self.__dispathQueue(value))
        res = redisConn().getInstance().lpush(key, value)
        return res

    def lrem(self, desc_key, count, desc_value):
        if not desc_key:
            return False
        return redisConn().getInstance().lrem(desc_key, count, desc_value)

    def __getPayRedisKey(self, index):
        return '%s%s' % (self.queue_prefix, index)

    def __dispathQueue(self, value):
        if(not value):
            return false
        first_value = value.split(self.queue_val_split)
        first_value = first_value[0].encode('UTF-8')
        encrty = hashlib.md5(first_value).hexdigest()
        return ord(encrty[0:1]) % self.notify_queue_num

    def update(self, order_no, is_notify, notify_time):
        if(not order_no):
            return False
        sql = 'update comm_payment.app_order set is_notify=%s, notify_time=%s where order_no=%s limit 1'
        res = dbConn().insertUpdate(sql, [is_notify, notify_time, order_no]);
        return res

    def addLog(self, order_no, d_dict, l_type):
        content = json.dumps(d_dict)
        ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_params = [order_no, content, l_type, ctime]
        if(not order_no):
            return False
        sql = 'insert into comm_payment.app_logs (`order_no`, `content`, `type`, ctime) values(%s,%s,%s,%s)'
        res = dbConn().insertUpdate(sql, log_params)
        return dbConn().getLastId()