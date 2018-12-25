import random

import pymysql


class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxys = self.get_random_proxy()
        proxy = random.choice(proxys)
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        conn = pymysql.connect(host="localhost", user="root", passwd="123456", db="ips", charset="utf8")
        cursor = conn.cursor()
        sql = "select * from ip_pool  LIMIT 0,150"
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        conn.close()
        ips = []
        for data in datas:
            ips.append('http://'+data[1])

        return ips