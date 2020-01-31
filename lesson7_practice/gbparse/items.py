# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class NumbersItem(scrapy.Item):
    _id = scrapy.Field()
    number = scrapy.Field()
    file = scrapy.Field()

class NotReadedItem(scrapy.Item):
    _id = scrapy.Field()
    number = scrapy.Field()
    file = scrapy.Field()