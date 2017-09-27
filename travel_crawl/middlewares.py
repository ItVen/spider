# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random  
from scrapy import log 

  
    

class TravelCrawlSpiderMiddleware(object):
   
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print("this is response ip-----:"+proxy)
        response.meta['proxy'] = proxy
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(request, response, exception, spider):
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip---------------:"+proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy 
            return request
        return response 

    def process_start_requests(start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def get_random_proxy(self):  
        '''随机从文件中读取proxy'''  
        while 1:  
            with open('proxies.txt', 'r') as f:  
                proxies = f.readlines()  
            if proxies:  
                break  
            else:  
                time.sleep(1)  
        proxy = random.choice(proxies).strip()  
        return proxy  



