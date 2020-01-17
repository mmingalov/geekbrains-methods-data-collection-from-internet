# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#Domain.User.Password for Local Service is:
# PC.MongoDB.P@$$w0rd

from pymongo import MongoClient

mongo_client = MongoClient() #localhost и стандартный порт, если подключаемся к локальному хосту

#класс отвечает за сохранение данных в базу
# class GbparsePipeline(object):
#     # паук передает данные (item) сюда
#     def process_item(self, item, spider):
#         database = mongo_client[spider.name]
#         collection = database['gb_parse_14_01']
#         collection.insert_one(item) #для списка объектов можно использовать insert_many
#         return item

class avitoparsePipeline(object):
    def process_item(self, item, spider):
        database = mongo_client[spider.name]
        collection = database['av_parse_16_01']
        collection.insert_one(item)
        return item