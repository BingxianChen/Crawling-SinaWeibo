# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from cookies import cookies


class CookiesMiddleware(object):

    """ 获取cookies """
    def process_request(self, request, spider):
        request.cookies = {'_T_WM': '0273b3ad144da525251c8a0253e4373b', 'SUHB': '0M2Fr6MMCDrhMy', 'SCF': 'Al2lFzwzwVLm1T5MoLA03U8uQB2sARdkHkYdvYmee6ujKc1s', 'SUB': '_2A250ZLfkDeRhGeNL71EX9y_EyDqIHXVXptmsrDV6PUJbkdANLUajkW1HZZzSuFZsSEG9OJtzjx6e_z9v5A..'}

class UserAgentMiddleware(object):
    """ 换User-Agent """

    def process_request(self, request, spider):
        request.headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'


class SinacrawSpiderMiddleware(object):
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

