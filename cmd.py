import sys
import time
from apiModel import apiModel
from queModel import queModel
from redisConn import redisConn
from apiModel import apiModel
from dbConn import dbConn

redis_key = sys.argv[1]
redis_des_key = queModel.queue_tmp_bak + redis_key[redis_key.rfind('_')+1:]
secodes = queModel.steps
max_counts = len(secodes)
while True:
    try:
        order_str = queModel().getInstance().getQueueDesBlock(redis_key, redis_des_key)
        des_key_value = order_str
    except Exception as err:
        redisConn().clear(err)
    if(order_str):
        L = order_str.decode().split(queModel.queue_val_split)
        order_no = L[0]
        pay_time = int(L[1])
        count = L[2]
        sys_time = int(time.time())
        if(int(count) > max_counts):
            queModel().getInstance().addLog(order_no, {'line':sys._getframe().f_lineno,'order_str':order_str}, 'cmd_moreMax')
        else:
            if(count not in secodes.keys()):
                continue

            if(sys_time - pay_time >= secodes[count]):
                try:
                    result = apiModel().getInstance().notifyOrder(order_no)

                except Exception as e:
                    dbConn().clear(e)
                    result = apiModel().getInstance().notifyOrder(order_no)

                if(result != apiModel().getInstance().notify_return):
                    res = queModel().getInstance().repushQueue(order_no, pay_time, int(count)+1)
                    queModel().getInstance().lrem(redis_des_key, 1, des_key_value)
                    if(not res):
                        queModel().getInstance().addLog(order_no, {'line':sys._getframe().f_lineno,'order_str':order_str}, 'cmdRepushFail')

                else:
                    res = queModel().getInstance().update(order_no, apiModel.is_notify_success, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    if (not res):
                        queModel().getInstance().addLog(order_no, {'line':sys._getframe().f_lineno,'order_str':order_str.decode(), 'res':res}, 'cmdRepushFail')
                    else:
                        queModel().getInstance().lrem(redis_des_key, 1, des_key_value)
            else:
                queModel().getInstance().repushQueue(order_no, pay_time, count)
                queModel().getInstance().lrem(redis_des_key, 1, des_key_value)
    else:
        print('no order_str', order_str)

    time.sleep(0.5)




