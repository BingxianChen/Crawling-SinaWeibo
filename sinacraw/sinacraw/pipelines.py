# -*- coding: utf-8 -*-

from sinacraw.items import InfoItem
from pymongo import MongoClient
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinacrawPipeline(object):

    def __init__(self):
        client = MongoClient("115.28.218.152",27017)
        client.craw.authenticate("xuan","11001724")
        db = client.craw
        self.coll = db.BFS

    def process_item(self, item, spider):
        if isinstance(item, InfoItem):
            info = dict(item)
            self.coll.insert(info)

        return item
