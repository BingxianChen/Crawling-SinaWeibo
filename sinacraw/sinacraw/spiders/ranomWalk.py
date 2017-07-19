# # encoding=utf-8
# import re
# import scrapy
# from scrapy.selector import Selector
# from scrapy.http import Request
# from sinacraw.items import InfoItem
#
# class random_walk(scrapy.Spider):
#     name = "randomWalk"
#     start_urls = ["http://weibo.cn/u/1890493665",]
#
#     # def start_requests(self):
#     #   yield Request(url="http://weibo.cn/u/1890493665",cookies={'_T_WM': '5ef79043e75fb23eedf4ee4c54775d3b', 'SUHB': '0LcS-B2tfa2ptP', 'SCF': 'AjbaUVTeiH3Djsh9a2jxHETgzDvMLg-XsrMxAL09w9weHHWuY4OTbwQ0dte8Dne08smCCELGbVBzUuhGQ0qFJGs.', 'SUB': '_2A2518cudDeRhGeNL71EX9y_EyDqIHXVXHdXVrDV6PUJbkdBeLXjekW0ZpyjRPPDl-M8JcZlw9JvUZC54-Q..'})
#
#
#     def parse(self, response):
#         selector = Selector(response)
#         text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
#         info = InfoItem()
#         if text0:
#             num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
#             num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
#             num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数
#             # print "微博数",num_tweets[0]
#             # print "关注数",num_follows[0]
#             # print "粉丝数",num_fans[0]
#             info['num_tweets'] = num_tweets[0]
#             info['num_follows'] = num_follows[0]
#             info['num_fans'] = num_fans[0]
#
#         url_information1 = "http://weibo.cn/%s/info" % 1890493665
#         yield Request(url=url_information1, meta={"item":info},callback=self.parse1)
#
#     def parse1(self, response):
#
#         selector = Selector(response)
#         infoItem = response.meta["item"]
#         text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
#         nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
#         gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
#         place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
#         signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
#         birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
#         sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
#         marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
#         url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接
#
#         # print "昵称",nickname[0]
#         # print "性别",gender[0]
#         # print "地区（包括省份和城市）",place[0]
#         # print "个性签名",signature[0]
#         # print "生日",birthday
#         # print "性取向",sexorientation
#         # print "婚姻状况",marriage
#         # print "首页链接",url[0]
#
#         infoItem['nickname'] = nickname[0]
#         infoItem['gender'] = gender[0]
#         infoItem['place'] = place[0]
#         infoItem['signature'] = signature[0]
#         infoItem['birthday'] = birthday
#         infoItem['sexorientation'] = sexorientation
#         infoItem['marriage'] = marriage
#         infoItem['url'] = url[0]
#
#         print 1
#         yield infoItem
#
