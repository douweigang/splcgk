
from wit.util import get_random_proxy

class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = get_random_proxy()
        # print(proxy)
        # proxy = random.choice(proxys)
        print("this is request ip:" + proxy.get("http"),request.url)
        request.meta['proxy'] = proxy.get("http")

