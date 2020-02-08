# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


class GraphItem(scrapy.Item):
    _id = scrapy.Field()
    user1 = scrapy.Field()
    user2 = scrapy.Field()
    graph_id = scrapy.Field()
    graph_username = scrapy.Field()