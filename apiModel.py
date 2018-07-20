import hashlib
from base import baseModel
from urllib import request
from urllib import parse
from dbConn import dbConn

class apiModel(baseModel):
    is_notify_success = 1
    notify_return = 'SUCCESS'
    return_params = ['order_no','trade_no','trade_type','goods_id','attach','money','paid_time','pay_total_price']

    def getInstance(self):
        return super(apiModel, self).getInstance(self.__class__)

    def makeSign(self, str, key):
        s = '%s&key=%s' % (str, key)
        s = s.encode('UTF-8')
        s = hashlib.md5(s).hexdigest()
        return s.upper()

    def getSignContent(self, dict, is_urlencode = False):
        if(not dict):
            return ''
        list_tup = sorted(dict.items(), key=lambda x:x[0]) #sorted(list1.items(), key=lambda x:x[0], reverse=True)
        s = ''
        for x in list_tup:
            if x[0] != "sign" and x[1] != "":
                if is_urlencode:
                    s = s + str(x[0]) + "=" + parse.quote(str(x[1])) + "&"
                else:
                    s = s + str(x[0]) + "=" + str(x[1]) + "&"

        return s[:-1]

    def notifyOrder(self, order_no):
        if not order_no:
            return False
        db_con = dbConn()
        sql = 'select * from comm_payment.app_order where order_no=%s limit 1'
        order_info = db_con.getFetchOne(sql, [order_no])
        if(not order_info):
            return False

        if(order_info['is_notify'] == self.is_notify_success):
            return self.notify_return

        if(not order_info['notify_url']):
            return False

        # jn = ','
        # jn = jn.join(self.return_params)

        sql = 'select * from comm_payment.app_type where id=%s limit 1'
        id_config = db_con.getFetchOne(sql, [order_info['app_type_id']])
        key = id_config['sign_key']

        return_params = {}
        for x in self.return_params:
            return_params[x] = order_info[x]

        s = self.getSignContent(return_params)
        return_params['sign'] = self.makeSign(s, key)
        data = parse.urlencode(return_params).encode('utf-8')
        try:
            f = request.urlopen(order_info['notify_url'], data)
        except Exception as err:
            print(err)
            return False
        return f.read().decode('utf-8')

