# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):
    """
        a useragent middleware which rotate the user agent when crawl websites

        if you set the USER_AGENT_LIST in settings,the rotate with it,if not,then use the default user_agent_list attribute instead.
    """

    # the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    # for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',
        'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        ]

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def _user_agent(self, spider):
        if hasattr(spider, 'user_agent'):
            return spider.user_agent
        elif self.user_agent:
            return self.user_agent

        return random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        ua = self._user_agent(spider)
        if ua:
            request.headers.setdefault('User-Agent', ua)

class EbksspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
