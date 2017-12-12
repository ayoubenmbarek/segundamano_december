# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import os
import random
import telnetlib
import logging
import time
from scrapy.exceptions import DropItem
#from scrapy import log
#from math import log  
import json
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.conf import settings
from settings import USER_AGENT_LIST

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        if random.choice(xrange(1,100)) <= 30:
	    #os.system("/etc/init.d/polipo stop")
	    #time.sleep(1)
	    #os.system("/etc/init.d/polipo start")
	    #time.sleep(2)
	    #logger.info('>>>> restart polipo')
	    logger = logging.getLogger(__name__)
	    logger.info('>>>> Changing UserAgent')	
            #log.msg('Changing UserAgent')
            ua  = random.choice(USER_AGENT_LIST)
            if ua:
                request.headers.setdefault('User-Agent', ua)
		logger = logging.getLogger(__name__)
		logger.info('>>>> UserAgent changed')
            	#log.msg('>>>> UserAgent changed')
    #def process_request(self, request, spider): #old
     #   ua  = random.choice(settings.get('USER_AGENT_LIST'))
      #  if ua:
       #     request.headers.setdefault('User-Agent', ua)
	

class ProxyMiddleware(object): #commented 3 july
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')


# 15% ip change
class RetryChangeProxyMiddleware(object):
    def process_request(self, request, spider):
        if random.choice(xrange(1,100)) <= 15:
            logger = logging.getLogger(__name__)
            #os.system("/etc/init.d/polipo stop")
	    logger.info('>>>> Changing proxy')
	    #os.system("service polipo restart") #to try next crawl
            #log.msg('Changing proxy')
            tn = telnetlib.Telnet('127.0.0.1', 9051)#this port change the proxy successfully
            tn.read_until("Escape character is '^]'.", 2)
            tn.write('AUTHENTICATE "<PASSWORD HERE>"\r\n')
            tn.read_until("250 OK", 2)
            tn.write("signal NEWNYM\r\n")
            tn.read_until("250 OK", 2)
            tn.write("quit\r\n")
            tn.close()
	    logger = logging.getLogger(__name__)
	    logger.info('Proxy changed. or9od chweya')
	    #os.system("service polipo restart") #to try next crawl
	    #os.system("service polipo restart") #to try next crawl
	    #os.system("/etc/init.d/polipo start")
            #log.msg('>>>> Proxy changed. or9od chweya')
            time.sleep(5)#default 10 changed on 07/07

class SegundamanoSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
