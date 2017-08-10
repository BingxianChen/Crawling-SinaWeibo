# encoding=utf-8
import re
import scrapy
import datetime
import random
from scrapy.selector import Selector
from scrapy.http import Request
from sinacraw.items import InfoItem

class mhrw_walk(scrapy.Spider):
    name = "MHRW"
    count = 0
    friends_id = set()  # 某用户的好友ID
    degree_v = 10
    ID_v = 6156171735
    url_main_v = "http://weibo.cn/u/%s"
    fans_finish = False
    follows_finish = False
    def start_requests(self):

        ID = 6156171735
        url_main = "http://weibo.cn/u/%s" % ID
        url_fans = "http://weibo.cn/%s/fans" % ID
        url_follows = "http://weibo.cn/%s/follow" % ID
        # 将有向图当做无向图处理

        yield Request(url=url_fans, dont_filter=True, meta={"url_main":url_main,"ID":ID}, callback=self.parse3_fans)  # 去爬粉丝
        yield Request(url=url_follows, dont_filter=True, meta={"url_main":url_main,"ID":ID}, callback=self.parse3_follows)  # 去爬关注人


    def parse(self, response):
        selector = Selector(response)
        ID = response.meta["ID"]
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

        url_information1 = "http://weibo.cn/%s/info" % ID
        yield Request(url=url_information1, meta={"item":info,"ID":ID}, dont_filter=True, callback=self.parse1)




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

        # 获取当前用户的好友数量 粉丝数 + 关注数
        degree_u = infoItem['num_follows'] + infoItem['num_fans']

        yield infoItem

        ############ MHRW算法 #########


        P = random.random()
        while True:
            # 获取随机访问下一用户的好友数量, 若下一用户不能获取则重复这行这步
            while True:
                try:
                    self.ID_v = random.choice(list(self.friends_id))
                    print self.ID_v
                    url_main = "http://weibo.cn/u/%s" % self.ID_v
                    yield Request(url=url_main, meta={"ID":self.ID_v}, dont_filter=True, callback=self.parse4)
                    if self.degree_v:
                        break
                except:
                    continue

            if P < float(degree_u)/self.degree_v:
                self.url_main_v = "http://weibo.cn/u/%s" % self.ID_v
                break
            else:
                yield infoItem

        url_fans = "http://weibo.cn/%s/fans" % self.ID_v
        url_follows = "http://weibo.cn/%s/follow" % self.ID_v
        # 将有向图当做无向图处理
        self.friends_id.clear()
        self.follows_finish = False
        self.fans_finish = False
        yield Request(url=url_fans, dont_filter=True, meta={"url_main":self.url_main_v,"ID":self.ID_v}, callback=self.parse3_fans)  # 去爬粉丝
        yield Request(url=url_follows, dont_filter=True, meta={"url_main":self.url_main_v,"ID":self.ID_v}, callback=self.parse3_follows)  # 去爬关注人




    def parse3_fans(self, response):
        """ 抓取关注或粉丝的随机用户ID """
        selector = Selector(response)
        text2 = selector.xpath('body//table/tr/td/a/@href').extract()
        url_main = response.meta["url_main"]
        ID_ = response.meta["ID"]
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                ID = int(elem[0])
                if ID not in self.friends_id:  # 新的ID，如果未爬则加入待爬队列
                    self.friends_id.add(ID)
        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url="http://weibo.cn%s" % url_next[0], meta={"url_main":url_main,"ID":ID_}, callback=self.parse3_fans)
        else:
            self.fans_finish = True
            if self.fans_finish and self.follows_finish:
                yield Request(url=url_main, meta={"ID":ID_}, dont_filter=True, callback=self.parse)

    def parse3_follows(self, response):
        """ 抓取关注或粉丝的随机用户ID """
        selector = Selector(response)
        text2 = selector.xpath('body//table/tr/td/a/@href').extract()
        url_main = response.meta["url_main"]
        ID_ = response.meta["ID"]
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                ID = int(elem[0])
                if ID not in self.friends_id:  # 新的ID，如果未爬则加入待爬队列
                    self.friends_id.add(ID)
        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url="http://weibo.cn%s" % url_next[0], meta={"url_main":url_main,"ID":ID_}, callback=self.parse3_follows)
        else:
            self.follows_finish = True
            if self.fans_finish and self.follows_finish:
                yield Request(url=url_main, meta={"ID":ID_}, dont_filter=True, callback=self.parse)



    def parse4(self, response):
        """ 获取下一访问用户的好友数量 """
        selector = Selector(response)
        text0 = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if text0:
            num_follows = re.findall(u'\u5173\u6ce8\[(\d+)\]', text0)  # 关注数
            num_fans = re.findall(u'\u7c89\u4e1d\[(\d+)\]', text0)  # 粉丝数

            if num_follows and num_fans:
                self.degree_v = num_fans + num_follows
            else:
                self.degree_v = False


