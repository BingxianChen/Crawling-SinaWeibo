# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinacrawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InfoItem(scrapy.Item):

    num_tweets = scrapy.Field()  # 微博数
    num_follows = scrapy.Field()  # 关注数
    num_fans = scrapy.Field()  # 粉丝数

    nickname = scrapy.Field()  # 获取标签里的所有text()
    gender = scrapy.Field()  # 昵称
    place = scrapy.Field()  # 地区（包括省份和城市）
    signature = scrapy.Field()  # 个性签名
    birthday = scrapy.Field()  # 生日
    sexorientation = scrapy.Field()  # 性取向
    marriage = scrapy.Field()  # 婚姻状况
    url = scrapy.Field()  # 首页链接


