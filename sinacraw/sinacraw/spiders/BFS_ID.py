# # encoding=utf-8
# import re
# import scrapy
# import datetime
# from collections import deque
# from scrapy.selector import Selector
# from scrapy.http import Request
# from sinacraw.items import InfoItem
#
# class random_walk(scrapy.Spider):
#     name = "BFS_ID"
#     count = 0
#     scrawl_ID = set(3762709983)  # 记录待爬的微博ID
#     finish_ID = set()  # 记录已爬的微博ID
#     def start_requests(self):
#         while True:
#             ID = self.scrawl_ID.pop()
#             self.finish_ID.add(ID)
#             url_fans = "http://weibo.cn/%s/fans" % ID
#             url_follows = "http://weibo.cn/%s/follow" % ID
#             # 将有向图当做无向图处理
#             yield Request(url=url_fans, dont_filter=True, callback=self.parse3)  # 去爬粉丝
#             yield Request(url=url_follows, dont_filter=True, callback=self.parse3)  # 去爬关注人
#
#
#     def parse3(self, response):
#         """ 抓取关注或粉丝的随机用户ID """
#         selector = Selector(response)
#         text2 = selector.xpath('body//table/tr/td/a/@href').extract()
#
#         for elem in text2:
#             elem = re.findall('uid=(\d+)', elem)
#             if elem:
#                 ID = int(elem[0])
#                 if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
#                     self.scrawl_ID.add(ID)
#         print self.scrawl_ID
#         url_next = selector.xpath(
#             u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
#         if url_next:
#             yield Request(url="http://weibo.cn%s" % url_next[0], callback=self.parse3)