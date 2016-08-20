# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QsbkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id=scrapy.Field()
    url=scrapy.Field()
    author=scrapy.Field()
    userlink=scrapy.Field()
    author_img=scrapy.Field()
    img=scrapy.Field()
    text=scrapy.Field()
