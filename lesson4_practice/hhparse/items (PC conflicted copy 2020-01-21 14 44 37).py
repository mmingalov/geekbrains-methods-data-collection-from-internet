# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

#задаем какие поля будут сохраняться
class hhparseItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    salary = scrapy.Field()
    skills = scrapy.Field()
    company_name = scrapy.Field()
    company_link = scrapy.Field()
    pass
