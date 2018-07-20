# coding=UTF-8
import sys
import pymysql
class dbConn:
    __instance = None
    db = None
    cursor = None
    def __new__(self):
        if self.__instance:
            return self.__instance
        self.__instance = object.__new__(self)
        self.__instance.__setConnent("localhost", "root", "123456")
        return self.__instance

    def __setConnent(self, host, user, pwd):
        try:
            self.db = pymysql.connect(host, user, pwd)
            self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            return self.db
        except Exception as err:
            raise

    def getFetchAll(self, sql, params_list = None):
        try:
            if params_list:
                self.cursor.execute(sql, params_list)
            else:
                self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.db.commit()
            return results
        except Exception as err:
            raise ValueError(err.args[1] + ' : ' + sql)


    def getFetchOne(self, sql, params_list = None):
        try:
            if params_list:
                self.cursor.execute(sql, params_list)
            else:
                self.cursor.execute(sql)
            results = self.cursor.fetchone()
            self.db.commit()
            return results
        except Exception as err:
            raise ValueError(err.args[1] + ' : ' + sql)

    def insertUpdate(self, sql, params_list = None):
        try:
            if params_list:
                sta = self.cursor.execute(sql, params_list)
            else:
                sta = self.cursor.execute(sql)
            self.db.commit()
            return sta
        except Exception as err:
            raise ValueError(err.args[1] + ' : ' + sql)

    def getLastId(self):
        return self.cursor.lastrowid

    def clear(self, error):
        print(__file__,sys._getframe().f_lineno,error)
        self.__instance.__setConnent("localhost", "root", "123456")



if __name__ == '__main__':
    try:
        obj = dbConn();
        sql = 'select * from db_netbar.t_bet_lol_log';
        results = obj.getFetchAll(sql)
        for row in results:
            did = row['id']
            user_id = row['user_id']
            netbar_id = row['netbar_id']
            dtype = row['type']
            business_type = row['business_type']
            diamonds = row['diamonds']
            score = row['score']
            dctime = row['ctime']
            print ("id=%s,user_id=%s,netbar_id=%s,type=%s,business_type=%d,diamonds=%d,score=%d,ctime=%s" % (did, user_id, netbar_id, dtype, business_type, diamonds, score, dctime ))
    except Exception as err:
        print(err)
    #db.close()
    # 关闭数据库连接
