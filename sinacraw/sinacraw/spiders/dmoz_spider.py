# encoding=utf-8
import re
import scrapy
import random
import datetime
from scrapy.selector import Selector
from scrapy.http import Request
from sinacraw.items import InfoItem

class random_walk(scrapy.Spider):
    name = "randomWalk"
    next_ID = [1890493665,]
    count = 0
    def start_requests(self):
        self.count += 1
        print "start!!!!!!!"
        next_url = "http://weibo.cn/u/%s" % self.next_ID[-1]
        yield Request(url=next_url, callback=self.parse)


    def parse(self, response):
        selector = Selector(response)
        text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        info = InfoItem()
        if text0:
            num_tweets = re.findall(u'\u5fae\u535a\[(\d+)\]', text0)  # 微博数
            num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
            num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数

            if num_tweets:
                info["num_tweets"] = int(num_tweets[0])
            if num_follows:
                info["num_follows"] = int(num_follows[0])
            if num_fans:
                info["num_fans"] = int(num_fans[0])

        url_information1 = "http://weibo.cn/%s/info" % self.next_ID[-1]
        yield Request(url=url_information1, meta={"item":info,"ID":self.next_ID[-1]}, dont_filter=True, callback=self.parse1)


        # 将有向图当做无向图处理
        if random.random() >= float(info["num_follows"])/(info["num_follows"] + info["num_fans"]):
            url_fans = "http://weibo.cn/%s/fans" % self.next_ID[-1]
            yield Request(url=url_fans, dont_filter=True, callback=self.parse3)  # 去爬粉丝
        else:
            url_follows = "http://weibo.cn/%s/follow" % self.next_ID[-1]
            yield Request(url=url_follows, dont_filter=True, callback=self.parse3)  # 去爬关注人


    def parse1(self, response):

        selector = Selector(response)
        infoItem = response.meta["item"]
        ID = response.meta["ID"]
        text1 = ";".join(selector.xpath('body/div[@class="c"]/text()').extract())  # 获取标签里的所有text()
        nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', text1)  # 昵称
        gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', text1)  # 性别
        place = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', text1)  # 地区（包括省份和城市）
        signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
        birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
        sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
        marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
        url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接

        if nickname:
            infoItem['nickname'] = nickname[0]
        if gender:
            infoItem['gender'] = gender[0]
        if place:
            place = place[0].split(" ")
            infoItem["province"] = place[0]
            if len(place) > 1:
                infoItem["city"] = place[1]
        if signature:
            infoItem["signature"] = signature[0]
        if birthday:
            try:
                birthday = datetime.datetime.strptime(birthday[0], "%Y-%m-%d")
                infoItem["birthday"] = birthday - datetime.timedelta(hours=8)
            except Exception:
                pass
        if sexorientation:
            if sexorientation[0] == gender[0]:
                infoItem["sexorientation"] = "gay"
            else:
                infoItem["sexorientation"] = "Heterosexual"
        if marriage:
            infoItem["marriage"] = marriage[0]
        if url:
            infoItem["url"] = url[0]

        infoItem["user_id"] = ID

        yield infoItem



    def parse3(self, response):
        """ 抓取关注或粉丝的随机用户ID """
        selector = Selector(response)
        text2 = selector.xpath('body//table/tr/td/a/@href').extract()
        next_urls = []
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                next_urls.append(int(elem[0]))

        self.next_ID.pop()
        self.next_ID.append(random.choice(next_urls))


        print "*********"
        print self.next_ID[-1]
        print "*********"

        next_url = "http://weibo.cn/u/%s" % self.next_ID[-1]
        yield Request(url=next_url, dont_filter=True, callback=self.parse)

