# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_salary(values):
    return ''.join(values).replace('\xa0','')   # сливаем список в текст и заменяем символ

def modify_link(link):
    v = link[0]
    prefix = 'https://vladivostok.hh.ru'
    if v[:1]=='/':
        result = prefix + v
    else:
        result = v
    return result

#задаем какие поля будут сохраняться
class hhparseItem(scrapy.Item):

    _id = scrapy.Field()
    url = scrapy.Field(output_processor = TakeFirst())
    title = scrapy.Field(output_processor = TakeFirst())
    salary = scrapy.Field(output_processor=cleaner_salary)
    skills = scrapy.Field()
    company_name = scrapy.Field(output_processor = TakeFirst())
    # company_link = scrapy.Field(input_processor = MapCompose(modify_link)) #сохраняет в список
    company_link = scrapy.Field(output_processor=modify_link)

    # url = scrapy.Field()
    # title = scrapy.Field()
    # salary = scrapy.Field()
    # skills = scrapy.Field()
    # company_name = scrapy.Field()
    # company_link = scrapy.Field()

    pass
