# -*- coding: utf-8 -*-

from sinacraw.items import DegreeItem, InfoItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinacrawPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,DegreeItem):
            print 1
        if isinstance(item,InfoItem):
            print 2
        return item
